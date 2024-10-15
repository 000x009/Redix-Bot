import json
import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi_cache.decorator import cache

from aiogram.utils.web_app import WebAppInitData

from src.schema import RawPromo
from src.services import PromoService, UserService, TransactionService
from src.schema.transaction import TransactionCause, TransactionType
from src.api.dependencies import user_provider
from src.schema import Promo


router = APIRouter(
    prefix="/promo",
    tags=["Promo"],
    route_class=DishkaRoute
)


@router.get('/')
@cache(expire=60 * 60 * 24)
async def get_promo(
    name: str,
    promo_service: FromDishka[PromoService],
) -> Optional[Promo]:
    promo = await promo_service.get_one_promo(name=name)
 
    return promo


@router.get('/check-used')
async def check_used(
    name: str,
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    user = await user_service.get_one_user(user_id=user_data.user.id)
    if user.used_coupons and name in user.used_coupons.get('coupons'):
        return JSONResponse(status_code=403, content='User already has used this promo')
 
    return JSONResponse(status_code=200, content='success')


@router.post('/')
async def use_promo(
    raw_promo: RawPromo,
    promo_service: FromDishka[PromoService],
    user_service: FromDishka[UserService],
    transaction_service: FromDishka[TransactionService],
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    promo = await promo_service.get_one_promo(name=raw_promo.name)
    if not promo:
        return JSONResponse(status_code=404, content='Promo not found')

    user = await user_service.get_one_user(user_id=user_data.user.id)
    used_coupons = user.used_coupons
    if used_coupons and raw_promo.name in used_coupons.get('coupons'):
        return JSONResponse(status_code=403, content='User already has used this promo')

    if used_coupons:
        used_coupons['coupons'].append(raw_promo.name) 
    else:
        used_coupons = {'coupons': [raw_promo.name]}
    
    if promo.uses <= 0:
        return JSONResponse(status_code=403, content='Promo is out of uses')

    updated_balance = user.balance + promo.bonus_amount
    if promo.uses == 1:
        await promo_service.delete_promo(name=raw_promo.name)
    else:
        await promo_service.update_promo(name=raw_promo.name, uses=promo.uses - 1)
    await user_service.update_user(user_id=user_data.user.id, used_coupons=used_coupons, balance=updated_balance)
    await transaction_service.add_transaction(
        id=uuid.uuid4(),
        user_id=user_data.user.id,
        type=TransactionType.DEPOSIT,
        cause=TransactionCause.COUPON,
        amount=promo.bonus_amount,
        is_successful=True,
    )

    return JSONResponse(status_code=200, content='success')
