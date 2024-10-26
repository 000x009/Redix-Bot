from typing import Optional, TypeAlias, List, Any
from uuid import UUID
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result, func, or_

from src.schema import Product
from src.data.models import ProductModel


_ProductResult: TypeAlias = Result[tuple[ProductModel]]


class ProductDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(ProductModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, product_id: UUID, **kwargs) -> None:
        query = update(ProductModel).where(ProductModel.id == product_id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, **kwargs: Optional[Any]) -> bool:
        query = select(exists(ProductModel))
        if kwargs:
            query = select(
                exists().where(
                    *(
                        getattr(ProductModel, key) == value
                        for key, value in kwargs.items()
                        if hasattr(ProductModel, key)
                    )
                )
            )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def is_column_filled(self, id: int, *column_names: str) -> bool:
        user_exists = await self.exists(id=id)
        if not user_exists:
            return False

        query = select(
            *(
                getattr(ProductModel, column_name)
                for column_name in column_names
                if hasattr(ProductModel, column_name)
            )
        ).where(ProductModel.id == id)

        result = await self.session.execute(query)
        column_value = result.scalar_one_or_none()
        return column_value is not None

    async def _get(self, **kwargs: Optional[Any]) -> Optional[_ProductResult]:
        exists = await self.exists(**kwargs)
        if not exists:
            return None

        query = select(ProductModel)
        if kwargs:
            query = select(ProductModel).filter_by(**kwargs)

        result = await self.session.execute(query)
        return result

    async def get_one(self, **kwargs: Optional[Any]) -> Optional[Product]:
        res = await self._get(**kwargs)

        if res:
            db_product = res.scalar_one_or_none()
            return Product(
                id=db_product.id,
                game_id=db_product.game_id,
                category_id=db_product.category_id,
                name=db_product.name,
                description=db_product.description,
                price=db_product.price,
                instruction=db_product.instruction,
                purchase_count=db_product.purchase_count,
                image_url=db_product.image_url,
                game_name=db_product.game_name,
                purchase_limit=db_product.purchase_limit,
                is_auto_purchase=db_product.is_auto_purchase,
                is_manual=db_product.is_manual,
                auto_purchase_text=db_product.auto_purchase_text,
                instruction_image_url=db_product.instruction_image_url,
            )

    async def get_all(self, **kwargs: Optional[Any]) -> Optional[List[Product]]:
        res = await self._get(**kwargs)

        if res:
            db_products = res.scalars().all()
            return [
                Product(
                    id=db_product.id,
                    name=db_product.name,
                    game_id=db_product.game_id,
                    description=db_product.description,
                    price=db_product.price,
                    instruction=db_product.instruction,
                    purchase_count=db_product.purchase_count,
                    game_name=db_product.game_name,
                    image_url=db_product.image_url,
                    category_id=db_product.category_id,
                    purchase_limit=db_product.purchase_limit,
                    is_auto_purchase=db_product.is_auto_purchase,
                    is_manual=db_product.is_manual,
                    auto_purchase_text=db_product.auto_purchase_text,
                    instruction_image_url=db_product.instruction_image_url,
                )
                for db_product in db_products
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(ProductModel).filter_by(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def search(self, search_name: str) -> Optional[List[Product]]:    
        search_term = f"%{search_name.lower()}%"
        query = (select(ProductModel)
            .where(or_(
            func.lower(ProductModel.name).like(search_term),
            func.lower(ProductModel.game_name).like(search_term),
            func.lower(ProductModel.category).like(search_term),
            func.lower(ProductModel.description).like(search_term),
            func.lower(ProductModel.instruction).like(search_term)
        )))

        res = await self.session.execute(query)
        products = res.scalars().all()

        return [
            Product(
                id=db_product.id,
                game_id=db_product.game_id,
                name=db_product.name,
                description=db_product.description,
                price=db_product.price,
                instruction=db_product.instruction,
                purchase_count=db_product.purchase_count,
                game_name=db_product.game_name,
                category_id=db_product.category_id,
                purchase_limit=db_product.purchase_limit,
                is_auto_purchase=db_product.is_auto_purchase,
                is_manual=db_product.is_manual,
                auto_purchase_text=db_product.auto_purchase_text,
                image_url=db_product.image_url,
                instruction_image_url=db_product.instruction_image_url,
            )
            for db_product in products
        ]

    async def get_purchase_count(self, days: Optional[int] = None) -> int:
        query = select(func.sum(ProductModel.purchase_count))
        if days:
            query = query.filter(ProductModel.created_at >= func.now() - timedelta(days=days))
        result = await self.session.execute(query)
        return result.scalar_one() or 0
    
    async def get_total_purchase_amount(self, days: Optional[int] = None) -> float:
        if days is not None:
            query = select(func.sum(ProductModel.price * ProductModel.purchase_count)).where(
                ProductModel.purchase_count > 0,
                ProductModel.purchase_count > func.now() - timedelta(days=days)
            )
        else:
            query = select(func.sum(ProductModel.price * ProductModel.purchase_count)).where(
                ProductModel.purchase_count > 0
            )
        result = await self.session.execute(query)

        return result.scalar_one_or_none() or 0.0
