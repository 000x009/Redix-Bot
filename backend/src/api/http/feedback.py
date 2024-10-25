import uuid
from datetime import datetime, UTC
from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from aiogram import Bot
from aiogram.types import BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.web_app import WebAppInitData

from src.services import FeedbackService, UserService, YandexStorageClient
from src.api.schema.feedback import CreateFeedback
from src.schema import Feedback
from src.api.dependencies import user_provider
from src.bot.app.main.config import dev_config
from src.api.http.exceptions import MethodNotAllowedError
from src.schema import User
from src.bot.app.main.config import settings

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
    route_class=DishkaRoute,
)


@router.post("/post", response_class=JSONResponse)
async def post_feedback(
    data: CreateFeedback,
    feedback_service: FromDishka[FeedbackService],
    yandex_storage_client: FromDishka[YandexStorageClient],
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    await feedback_service.add_feedback(
        id=uuid.uuid4(),
        product_id=data.product.id,
        order_id=data.order_id,
        user_id=user_data.user.id,
        text=data.text,
        stars=data.stars,
        time=datetime.now(tz=UTC),
        images=data.images,
    )
    feedback_group_id = 2348273294
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    media_group = MediaGroupBuilder(caption=f"""
Рейтинг: {"⭐" * data.stars}
Покупатель: @{user_data.user.username}
Дата: {datetime.now(tz=UTC).strftime("%d.%m.%Y %H:%M")}

Отзыв:
{data.text}
""")
    
    for image_url in data.images:
        image_content = yandex_storage_client.get_file(image_url)
        file = BufferedInputFile(image_content, filename=f"feedback_image_{uuid.uuid4()}.jpg")
        media_group.add_photo(media=file)
    
    await bot.send_media_group(chat_id=feedback_group_id, media=media_group.build())

    return JSONResponse(
        status_code=200,
        content=dict(detail='success')
    )


@router.get("/", response_model=List[Feedback])
async def get_feedbacks(
    feedback_service: FromDishka[FeedbackService],
) -> List[Feedback]:
    response = await feedback_service.get_feedbacks(is_active=True)
    return response


@router.get("/{feedback_id}", response_model=Feedback)
async def get_one_feedback(
    feedback_id: uuid.UUID,
    feedback_service: FromDishka[FeedbackService],
) -> Feedback:
    return await feedback_service.get_one_feedback(id=feedback_id)


@router.get("/is_user_posted_feedback/{order_id}")
async def is_user_posted_feedback(
    order_id: uuid.UUID,
    feedback_service: FromDishka[FeedbackService],
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[Feedback]:
    return await feedback_service.get_one_feedback(user_id=user_data.user.id, order_id=order_id)


@router.get("/remove/{feedback_id}", response_class=JSONResponse)
async def remove_feedback(
    feedback_id: uuid.UUID,
    feedback_service: FromDishka[FeedbackService],
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    if not user_data.user.id in dev_config.admin.admins:
        raise MethodNotAllowedError

    await feedback_service.delete_feedback(feedback_id=feedback_id)

    return JSONResponse(
        status_code=200,
        content=dict(detail='success')
    )


@router.get("/user/{user_id}", response_model=User)
async def get_user_feedbacks(
    user_id: int,
    user_service: FromDishka[UserService],
) -> User:
    return await user_service.get_one_user(user_id=user_id)
