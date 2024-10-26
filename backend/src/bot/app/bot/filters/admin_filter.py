from aiogram.types import Message
from aiogram.filters import BaseFilter

from src.services import AdminService


class AdminFilter(BaseFilter):
    def __init__(
        self,
        admin_service: AdminService,
    ) -> None:
        self.admin_service = admin_service

    async def __call__(self, message: Message) -> bool:
        admins = await self.admin_service.get_all()
        admin_ids = [admin.user_id for admin in admins]
        return message.from_user.id in admin_ids
    