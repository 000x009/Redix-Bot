from typing import Optional

from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppInitData

from fastapi import Request

from src.main.config import settings
from src.api.http.exceptions import NotAuthorizedError


async def user_provider(request: Request) -> Optional[WebAppInitData]:
    try:
        auth_string = request.headers.get('Authorization')
        if auth_string:
            return safe_parse_webapp_init_data(settings.BOT_TOKEN, auth_string)
        else:
            raise NotAuthorizedError(401, detail=dict(error='Not Authorized.'))
    except ValueError:
        raise NotAuthorizedError(401, detail=dict(error='Not Authorized.'))
