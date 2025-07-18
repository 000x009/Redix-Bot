from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dependency_injector.wiring import inject, Provide

from src.main.ioc import Container
from src.services import FragmentAPI, UserService
from src.data.dal import StarsDAL
from src.utils.user_provider import user_provider
from src.data.models.user import WebAppInitData
from src.utils import json_text_getter
from src.main.config import settings


class BuyStarsDTO(BaseModel):
    username: str
    quantity: int


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
) -> JSONResponse:
    stars_config = await stars_dal.get_one()
    if not stars_config:
        return JSONResponse(status_code=400, content=dict(message='Stars config not found'))
    
    fragment_service.set_hash_and_cookie(stars_config.api_hash, stars_config.api_cookie, stars_config.mnemonic)
    await fragment_service.buy_stars(data.username, data.quantity)

    user = await user_service.get_one_user(user_id=user_data.user.id)
    product = await product_service.get_one_product(id=order_data.product_id)
    game = await game_service.get_game(id=product.game_id)
    category = await category_service.get_category(id=product.category_id)

    if not product:
        return JSONResponse(status_code=404, content='Product not found.')
    elif not user:
        return JSONResponse(status_code=404, content='User not found.')
    elif user.balance < product.price:
        return JSONResponse(
            status_code=409,
            content=dict(
                description='Insufficient funds on user balance',
                user_balance=float(user.balance),
                top_up_amount=float(product.price - user.balance),
            )
        )
    
    order_id = uuid.uuid4()
    await order_service.add_order(
        id=order_id,
        user_id=user.user_id,
        product_id=order_data.product_id,
        name=product.name,
        price=product.price,
        additional_data=order_data.additional_data,
    )
    await user_service.update_user(user_id=user.user_id, balance=user.balance - product.price)
    await transaction_service.add_transaction(
        id=uuid.uuid4(),
        user_id=user.user_id,
        type=TransactionType.DEBIT,
        cause=TransactionCause.PAYMENT,
        amount=product.price,
        is_successful=True,
    )

    try:
        bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await bot.send_message(
            chat_id=game.supergroup_id,
            text=json_text_getter.get_order_info_text(
                user_id=user.user_id,
                order_id=order_id,
                order_data=order_data.additional_data,
                product=product,
                category=category.name,
            ),
            message_thread_id=category.thread_id,
            reply_markup=take_order_kb_markup(order_id=order_id)
        )
    except Exception as e:
        print(e)
    finally:
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
