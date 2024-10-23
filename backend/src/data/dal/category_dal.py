from typing import Optional, TypeAlias, List, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result

from src.schema import Category
from src.data.models import CategoryModel


_CategoryResult: TypeAlias = Result[tuple[CategoryModel]]


class CategoryDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def add(self, **kwargs) -> None:
        query = insert(CategoryModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, id: int, **kwargs) -> None:
        query = update(CategoryModel).where(CategoryModel.id == id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, **kwargs: Optional[Any]) -> CategoryModel:
        query = select(CategoryModel).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, **kwargs: Optional[Any]) -> List[CategoryModel]:
        if kwargs:
            query = select(CategoryModel).filter_by(**kwargs)
        else:
            query = select(CategoryModel)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete(self, id: int) -> None:
        query = delete(CategoryModel).where(CategoryModel.id == id)
        await self.session.execute(query)
        await self.session.commit()

