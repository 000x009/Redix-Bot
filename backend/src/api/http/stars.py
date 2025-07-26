from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dependency_injector.wiring import inject, Provide

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.web_app import WebAppInitData

from src.main.ioc import Container
from src.services import (
    FragmentAPI,
    UserService,
    ProductService,
    GameService,
    CategoryService,
    OrderService,
    TransactionService
)
from src.data.dal import StarsDAL
from src.api.dependencies import user_provider
from src.utils import json_text_getter
from src.main.config import settings
from src.schema.transaction import TransactionCause, TransactionType
from src.schema.order import OrderStatus
from src.services.fragment_r import buy_stars as buy_stars_r


class BuyStarsDTO(BaseModel):
    username: str
    quantity: int
    category_id: UUID


router = APIRouter(
    prefix="/stars",
    tags=["Stars"],
)


@router.post("/buy-stars")
@inject
async def buy_stars(
    data: BuyStarsDTO,
    stars_dal: StarsDAL = Depends(Provide[Container.stars_dal]),
    fragment_service: FragmentAPI = Depends(Provide[Container.fragment_service]),
    user_service: UserService = Depends(Provide[Container.user_service]),
    user_data: WebAppInitData = Depends(user_provider),
    product_service: ProductService = Depends(Provide[Container.product_service]),
    game_service: GameService = Depends(Provide[Container.game_service]),
    category_service: CategoryService = Depends(Provide[Container.category_service]),
    order_service: OrderService = Depends(Provide[Container.order_service]),
    transaction_service: TransactionService = Depends(Provide[Container.transaction_service]),
) -> JSONResponse:
    stars_config = await stars_dal.get_one()
    if not stars_config:
        return JSONResponse(status_code=400, content=dict(message='Stars config not found'))
    
    await buy_stars_r(
        username=data.username,
        quantity=data.quantity,
        cookie=stars_config.api_cookie,
        hash=stars_config.api_hash,
        mnemonic=stars_config.mnemonic
    )

    user = await user_service.get_one_user(user_id=user_data.user.id)
    product = await product_service.get_stars_product_by_category_id(category_id=data.category_id)
    game = await game_service.get_game(id=product.game_id)
    category = await category_service.get_category(id=data.category_id)
    price = data.quantity * stars_config.rate

    if not product:
        return JSONResponse(status_code=404, content='Product not found.')
    elif not user:
        return JSONResponse(status_code=404, content='User not found.')
    elif user.balance < price:
        return JSONResponse(
            status_code=409,
            content=dict(
                description='Insufficient funds on user balance',
                user_balance=float(user.balance),
                top_up_amount=float(float(round(price, 2)) - float(user.balance)),
            )
        )
    
    order_id = uuid4()
    await order_service.add_order(
        id=order_id,
        user_id=user.user_id,
        product_id=product.id,
        name=product.name,
        price=price,
        additional_data={"Telegram Stars": data.quantity, "Для Username": data.username},
        status=OrderStatus.COMPLETED,
    )
    await user_service.update_user(user_id=user.user_id, balance=float(user.balance) - float(round(price, 2)))
    await transaction_service.add_transaction(
        id=uuid4(),
        user_id=user.user_id,
        type=TransactionType.DEBIT,
        cause=TransactionCause.PAYMENT,
        amount=round(price, 2),
        is_successful=True,
    )

    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # try:
    print("SEND MESSAGE", flush=True)
    await bot.send_message(
        chat_id=game.supergroup_id,
        text=json_text_getter.get_order_info_text_stars(
            user_id=user.user_id,
            order_id=order_id,
            order_data={"Telegram Stars": data.quantity},
            product=product,
            category=category.name,
            username=data.username,
        ),
        message_thread_id=category.thread_id,
    )
    # except Exception as e:
    #     print(e, flush=True)
    # finally:
    await bot.session.close()

    return JSONResponse(status_code=200, content=dict(message="success"))


@router.get("/rate")
@inject
async def get_stars_rate(
    stars_dal: StarsDAL = Depends(Provide[Container.stars_dal]),
) -> JSONResponse:
    stars_config = await stars_dal.get_one()
    if not stars_config:
        return JSONResponse(status_code=400, content=dict(message='Stars rates not found'))
    return JSONResponse(status_code=200, content=dict(rate=float(stars_config.rate)))
