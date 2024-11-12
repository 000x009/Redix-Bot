import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from dependency_injector.wiring import inject, Provide

from aiogram import Bot
from aiogram.utils.web_app import WebAppInitData

from src.services import BileeService, TransactionService, UserService
from src.api.schema.payment import TopUpSchema
from src.api.dependencies import user_provider
from src.schema.transaction import TransactionCause, TransactionType
from src.main.config import settings
from src.main.ioc import Container

router = APIRouter(
    prefix="/payment",
    tags=["Payment System"],
)

 
@router.post('/')
@inject
async def top_up(
    data: TopUpSchema,
    bilee_service: BileeService = Depends(Provide[Container.bilee_service]),
    transaction_service: TransactionService = Depends(Provide[Container.transaction_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> dict:
    response = bilee_service.create_invoice(amount=data.amount, method=data.method.value)

    if response.get('success') is True:
        payment_data = response['payment']
        payment_data['url'] = response['url']
        await transaction_service.add_transaction(
            id=payment_data['uuid'],
            user_id=user_data.user.id,
            type=TransactionType.DEPOSIT,
            cause=TransactionCause.DONATE,
            amount=payment_data['amount'],
            payment_data=payment_data
        )

    return response

@router.post("/webhook", response_class=JSONResponse)
@inject
async def receive_payment(
    request: Request,
    transaction_service: TransactionService = Depends(Provide[Container.transaction_service]),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> JSONResponse:
    try:
        payload = await request.json()
        payment_id = payload.get('uuid')
        if not payment_id:
            return JSONResponse(status_code=400, content={"error": "Missing payment ID"})

        payment = await transaction_service.get_one_transaction(id=payment_id)
        if not payment:
            return JSONResponse(status_code=400, content={"error": "Payment not found"})

        user = await user_service.get_one_user(user_id=payment.user_id)
        top_up_amount = payload.get('amount')
        await user_service.update_user(user_id=user.user_id, balance=user.balance + top_up_amount)
        await transaction_service.update_transaction(id=payment_id, is_successful=True)

        try:
            bot = Bot(token=settings.BOT_TOKEN)
            await bot.send_message(chat_id=user.user_id, text=f"✅ Баланс пополнен на {top_up_amount} рублей")

            if user.referral_id:
                referral = await user_service.get_one_user(user_id=user.referral_id)
                reff_top_up_amount = round(top_up_amount * 0.02, 2)
                await user_service.update_user(user_id=user.referral_id, balance=referral.balance + reff_top_up_amount)
                await transaction_service.add_transaction(
                    id=uuid.uuid4(),
                    user_id=referral.user_id,
                    type=TransactionType.DEPOSIT,
                    cause=TransactionCause.REFERRAL,
                    amount=reff_top_up_amount,
                    is_successful=True,
                )
                bot = Bot(token=settings.BOT_TOKEN)
                await bot.send_message(chat_id=user.user_id, text=f"✅ Баланс пополнен на {reff_top_up_amount} рублей")
        except Exception as e:
            pass
        finally:
            await bot.session.close()

        return JSONResponse(status_code=200, content={"success": True})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})