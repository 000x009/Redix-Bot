from typing import Optional

from fastapi import APIRouter, Depends

from aiogram.utils.web_app import WebAppInitData
from dependency_injector.wiring import inject, Provide

from src.main.ioc import Container
from src.services import AdminService
from src.schema.admin import Admin
from src.api.dependencies import user_provider


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/")
@inject
async def get_admin(
    admin_service: AdminService = Depends(Provide[Container.admin_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[Admin]:
    admin = await admin_service.get(user_id=user_data.user.id)
    return admin
