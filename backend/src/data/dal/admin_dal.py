from typing import Optional, List, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, delete

from src.schema import Admin
from src.data.models import AdminModel


class AdminDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def add(self, **kwargs) -> None:
        query = insert(AdminModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, user_id: int, **kwargs) -> None:
        query = update(AdminModel).where(AdminModel.user_id == user_id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, **kwargs: Optional[Any]) -> Admin:
        query = select(AdminModel).filter_by(**kwargs)
        result = await self.session.execute(query)
        db_result = result.scalar_one_or_none()

        return Admin(
            id=db_result.id,
            user_id=db_result.user_id,
            role=db_result.role,
            permissions=db_result.permissions
        )

    async def get_all(self, **kwargs: Optional[Any]) -> List[Admin]:
        if kwargs:
            query = select(AdminModel).filter_by(**kwargs)
        else:
            query = select(AdminModel)
        result = await self.session.execute(query)
        results = result.scalars().all()

        return [
            Admin(
                id=result.id,
                user_id=result.user_id,
                role=result.role,
                permissions=result.permissions
            )
            for result in results
        ]

    async def delete(self, **kwargs) -> None:
        query = delete(AdminModel).filter_by(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

