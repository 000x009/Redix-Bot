import uuid
from datetime import datetime, UTC
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from aiogram.utils.web_app import WebAppInitData

from src.services import FeedbackService, UserService
from src.api.schema.feedback import CreateFeedback
from src.schema import Feedback
from src.api.dependencies import user_provider
from src.bot.app.main.config import dev_config
from src.api.http.exceptions import MethodNotAllowedError
from src.schema import User

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
    route_class=DishkaRoute,
)


@router.post("/post", response_class=JSONResponse)
async def post_feedback(
    data: CreateFeedback,
    feedback_service: FromDishka[FeedbackService],
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    await feedback_service.add_feedback(
        id=uuid.uuid4(),
        product_id=data.product.id,
        order_id=data.order_id,
        user_id=user_data.user.id,
        text=data.text,
        stars=data.stars,
        time=datetime.now(tz=UTC)
    )
    

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
) -> Feedback:
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
