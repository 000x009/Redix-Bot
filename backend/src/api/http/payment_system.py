import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from aiogram import Bot
from aiogram.utils.web_app import WebAppInitData

from dependency_injector.wiring import inject, Provide

from src.main.ioc import Container
from src.services import FreeKassaService, TransactionService, UserService
from src.api.schema.payment import TopUpSchema
from src.api.dependencies import user_provider
from src.schema.transaction import TransactionCause, TransactionType
from src.schema.transaction import Transaction
from src.main.config import settings

router = APIRouter(
    prefix="/payment",
    tags=["Payment System"],
)

 
@router.post('/', response_model=Transaction)
@inject
async def top_up(
    data: TopUpSchema,
    request: Request,
    freekassa_service: FreeKassaService = Depends(Provide[Container.freekassa_service]),
    transaction_service: TransactionService = Depends(Provide[Container.transaction_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> Transaction:
    print("PAYMENT METHOD", data.method)
    print("IP", request.client.host)
    transaction = await transaction_service.add_transaction(
        user_id=user_data.user.id,
        type=TransactionType.DEPOSIT,
        cause=TransactionCause.DONATE,
        amount=data.amount,
        is_successful=False,
    )
    response = freekassa_service.create_order(
        amount=data.amount,
        payment_method=data.method,
        ip=request.client.host,
        email="leonshevchenko616@gmail.com",
        unique_transaction_id=transaction.unique_id,
    )

    if response.get("type") == "success":
        payment_data = response
        # payment_data['url'] = response['location']
        await transaction_service.update_transaction(id=transaction.id, payment_data=payment_data)

    updated_transaction = await transaction_service.get_one_transaction(id=transaction.id)

    return updated_transaction


@router.post("/webhook", response_class=JSONResponse)
@inject
async def receive_payment(
    request: Request,
    transaction_service: TransactionService = Depends(Provide[Container.transaction_service]),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> JSONResponse:
    print("request", request)
    try:
        payload = await request.json()
        payment_id = payload.get('MERCHANT_ORDER_ID')
        if not payment_id:
            return JSONResponse(status_code=400, content={"error": "Missing payment ID"})

        payment = await transaction_service.get_one_transaction(id=payment_id)
        if not payment:
            return JSONResponse(status_code=400, content={"error": "Payment not found"})

        user = await user_service.get_one_user(user_id=payment.user_id)
        top_up_amount = float(payload.get('AMOUNT'))
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
                    user_id=referral.user_id,
                    type=TransactionType.DEPOSIT,
                    cause=TransactionCause.REFERRAL,
                    amount=reff_top_up_amount,
                    is_successful=True,
                )
                await bot.send_message(chat_id=referral.user_id, text=f"✅ Баланс пополнен на {reff_top_up_amount} рублей")
        except Exception as e:
            pass
        finally:
            await bot.session.close()

        return JSONResponse(status_code=200, content={"success": True})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    


@router.post("/success")
async def success_payment(request: Request):
    return JSONResponse(status_code=200, content={"success": True})


@router.post("/fail")
async def fail_payment(request: Request):
    return JSONResponse(status_code=200, content={"success": False})
