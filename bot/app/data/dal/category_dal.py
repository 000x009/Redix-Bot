from typing import Optional, List, Any
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, delete

from app.schema import Category
from app.data.models import CategoryModel, ProductModel


class CategoryDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def add(self, **kwargs) -> None:
        query = insert(CategoryModel).values(id=uuid.uuid4(), **kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, category_id: int, **kwargs) -> None:
        query = update(CategoryModel).where(CategoryModel.id == category_id).values(**kwargs)
        if kwargs.get('is_visible'):
            products_query = update(ProductModel).where(ProductModel.category_id == category_id).values(is_visible=kwargs['is_visible'])
            await self.session.execute(products_query)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, **kwargs: Optional[Any]) -> Category:
        query = select(CategoryModel).filter_by(**kwargs)
        result = await self.session.execute(query)
        db_result = result.scalar_one_or_none()

        return Category(
            id=db_result.id,
            game_id=db_result.game_id,
            name=db_result.name,
            image=db_result.image,
            is_visible=db_result.is_visible,
            thread_id=db_result.thread_id,
            web_app_place=db_result.web_app_place,
            required_fields=db_result.required_fields,
        )

    async def get_all(self, **kwargs: Optional[Any]) -> List[Category]:
        if kwargs:
            query = select(CategoryModel).filter_by(**kwargs).order_by(CategoryModel.web_app_place)
        else:
            query = select(CategoryModel).order_by(CategoryModel.web_app_place)
        result = await self.session.execute(query)
        results = result.scalars().all()

        return [
            Category(
                id=result.id,
                game_id=result.game_id,
                name=result.name,
                image=result.image,
                is_visible=result.is_visible,
                thread_id=result.thread_id,
                web_app_place=result.web_app_place,
                required_fields=result.required_fields,
            )
            for result in results
        ]

    async def delete(self, id: int) -> None:
        query = delete(CategoryModel).where(CategoryModel.id == id)
        await self.session.execute(query)
        await self.session.commit()

