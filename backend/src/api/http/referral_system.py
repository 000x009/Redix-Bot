from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.main.ioc import Container
from dependency_injector.wiring import inject, Provide

from aiogram.utils.web_app import WebAppInitData

from src.services import UserService
from src.api.schema.referral import ReferralCode, NewReferralCode
from src.main.config import settings
from src.api.dependencies import user_provider


router = APIRouter(
    prefix="/referral",
    tags=["Referral System"],
)


@router.get("/check_code_availability")
@inject
async def check_code(
    referral_code: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> JSONResponse:
    user = await user_service.get_one_user(referral_code=referral_code)
    if not user:
        return JSONResponse(status_code=200, content=dict(description='Code is available'))
    else:
        return JSONResponse(status_code=400, content=dict(description='Code is already taken'))


@router.get("/get_code", response_model=ReferralCode)
@inject
async def get_referral_code(
    user_service: UserService = Depends(Provide[Container.user_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> ReferralCode:
    user = await user_service.get_one_user(user_id=user_data.user.id)
    if not user:
        return JSONResponse(status_code=404, content="User not found")
    
    referral_url = settings.get_referral_url(user.referral_code)

    return ReferralCode(code=user.referral_code, referral_url=referral_url)


@router.post("/set_code")
@inject
async def set_code(
    referral_code: NewReferralCode,
    user_service: UserService = Depends(Provide[Container.user_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> ReferralCode:
    user = await user_service.get_one_user(user_id=user_data.user.id)
    if not user:
        return JSONResponse(status_code=404, content=dict(description='User not found'))
    elif user.referral_code == referral_code:
        return JSONResponse(status_code=400, content=dict(description='This referral code already in use by user.'))
    
    await user_service.update_user(user_id=user_data.user.id, referral_code=referral_code.referral_code)
    referral_url = settings.referral_url(referral_code)

    return ReferralCode(code=user.referral_code, referral_url=referral_url)