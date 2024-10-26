from typing import Optional

from fastapi import APIRouter, Depends

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from aiogram.utils.web_app import WebAppInitData

from src.services import AdminService
from src.schema.admin import Admin
from src.api.dependencies import user_provider


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    route_class=DishkaRoute,
)


@router.get("/")
async def get_admin(
    admin_service: FromDishka[AdminService],
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[Admin]:
    admin = await admin_service.get(user_id=user_data.user.id)
    return admin
