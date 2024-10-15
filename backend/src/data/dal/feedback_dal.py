from typing import Optional, TypeAlias, List, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result

from src.schema import Feedback
from src.data.models import FeedbackModel


_FeedbackResult: TypeAlias = Result[tuple[FeedbackModel]]


class FeedbackDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(FeedbackModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, id: int, **kwargs) -> None:
        query = update(FeedbackModel).where(FeedbackModel.id == id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, **kwargs: Optional[Any]) -> bool:
        if kwargs:
            query = select(
                exists().where(
                    *(
                        getattr(FeedbackModel, key) == value
                        for key, value in kwargs.items()
                        if hasattr(FeedbackModel, key)
                    )
                )
            )
        query = select(exists(FeedbackModel))
        result = await self.session.execute(query)
        return result.scalar_one()

    async def is_column_filled(self, user_id: int, *column_names: str) -> bool:
        user_exists = await self.exists(user_id=user_id)
        if not user_exists:
            return False

        query = select(
            *(
                getattr(FeedbackModel, column_name)
                for column_name in column_names
                if hasattr(FeedbackModel, column_name)
            )
        ).where(FeedbackModel.user_id == user_id)

        result = await self.session.execute(query)
        column_value = result.scalar_one_or_none()
        return column_value is not None

    async def _get(self, **kwargs: Optional[Any]) -> Optional[_FeedbackResult]:
        exists = await self.exists(**kwargs)
        if not exists:
            return None

        if kwargs:
            query = select(FeedbackModel).filter_by(**kwargs)
        else:
            query = select(FeedbackModel)

        result = await self.session.execute(query)
        return result

    async def get_one(self, **kwargs: Optional[Any]) -> Optional[Feedback]:
        res = await self._get(**kwargs)

        if res:
            db_feedback = res.scalar_one_or_none()
            return Feedback(
                id=db_feedback.id,
                product_id=db_feedback.product_id,
                order_id=db_feedback.order_id,
                user_id=db_feedback.user_id,
                text=db_feedback.text,
                stars=db_feedback.stars,
                time=db_feedback.time,
                is_active=db_feedback.is_active,
            )

    async def get_all(self, **kwargs: Optional[Any]) -> Optional[List[Feedback]]:
        res = await self._get(**kwargs)

        if res:
            db_feedbacks = res.scalars().all()
            return [
                Feedback(
                    id=db_feedback.id,
                    product_id=db_feedback.product_id,
                    order_id=db_feedback.order_id,
                    user_id=db_feedback.user_id,
                    text=db_feedback.text,
                    stars=db_feedback.stars,
                    time=db_feedback.time,
                    is_active=db_feedback.is_active,
                )
                for db_feedback in db_feedbacks
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(FeedbackModel).filter_by(**kwargs)
        await self.session.execute(query)
        await self.session.commit()
