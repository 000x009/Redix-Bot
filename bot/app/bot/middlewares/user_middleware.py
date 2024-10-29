from typing import Any, Awaitable, Callable, Dict

from dishka import AsyncContainer, Scope

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject, Message, User

from app.services import UserService
from app.main.config import settings


class UserMiddleware(BaseMiddleware):
    def __init__(self, dishka_container: AsyncContainer) -> None:
        self._dishka_container = dishka_container

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self._dishka_container(scope=Scope.REQUEST) as request_container:
            user_service = await request_container.get(UserService)

        user: User = data['event_from_user']
        bot = data['bot']
        exists = await user_service.exists(user_id=user.id)
        if not exists:
            reffer_id = None
            if isinstance(event, Message):
                start_command = event.text   
                if len(start_command) >= 7:
                    reffer_id = start_command[7:] if start_command[7:].isdigit() else None
                    reffer_id = reffer_id[4:]

            user_photos = await user.get_profile_photos()
            if user_photos.total_count > 0:
                photo = user_photos.photos[0][-1]
                file = await bot.get_file(photo.file_id)
                file_url = f"https://api.telegram.org/file/bot{settings.BOT_TOKEN}/{file.file_path}"
            else:
                file_url = None
                
            user_fullname = None
            if user.first_name and user.last_name:
                user_fullname = f"{user.first_name} {user.last_name}"
            elif user.first_name:
                user_fullname = user.first_name
            elif user.last_name:
                user_fullname = user.last_name
                
            await user_service.add_user(
                user_id=user.id,
                referral_code=str(user.id),
                referral_id=int(reffer_id) if reffer_id else None,
                nickname=user_fullname,
                profile_photo=file_url,
            )
        
        return await handler(event, data)
