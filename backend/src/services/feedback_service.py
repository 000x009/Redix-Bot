import uuid
from typing import Optional, Any, List

from src.data.dal import FeedbackDAL
from src.schema import Feedback


class FeedbackService:
    def __init__(self, feedback_dal: FeedbackDAL) -> None:
        self.__feedback_dal = feedback_dal

    async def get_feedbacks(self, **params: Optional[Any]) -> Optional[List[Feedback]]:
        return await self.__feedback_dal.get_all(**params)
    
    async def get_one_feedback(self, **params: Optional[Any]) -> Optional[Feedback]:
        return await self.__feedback_dal.get_one(**params)
    
    async def add_feedback(self, **params) -> None:
        await self.__feedback_dal.add(**params)

    async def update_feedback(self, feedback_id: int, **values) -> None:
        await self.__feedback_dal.update(id=feedback_id, **values)

    async def delete_feedback(self, feedback_id: uuid.UUID) -> None:
            await self.__feedback_dal.update(id=feedback_id, is_active=False)
