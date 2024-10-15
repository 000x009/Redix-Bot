from typing import Sequence, Optional

from aiogram.types import Message
from aiogram.filters import BaseFilter

from src.bot.app.main.config import dev_config


class AdminFilter(BaseFilter):
    def __init__(self, admin_ids: Optional[Sequence] = None) -> None:
        self.admin_ids = admin_ids if admin_ids else dev_config.admin.admins

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
    