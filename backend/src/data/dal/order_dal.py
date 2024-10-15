import uuid
from typing import Optional, TypeAlias, List, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result

from src.schema import Order
from src.data.models import OrderModel


_OrderResult: TypeAlias = Result[tuple[OrderModel]]


class OrderDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(OrderModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, order_id: uuid.UUID, **kwargs) -> None:
        query = update(OrderModel).where(OrderModel.id == order_id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, **kwargs: Optional[Any]) -> bool:
        if kwargs:
            query = select(
                exists().where(
                    *(
                        getattr(OrderModel, key) == value
                        for key, value in kwargs.items()
                        if hasattr(OrderModel, key)
                    )
                )
            )
        query = select(exists(OrderModel))
        result = await self.session.execute(query)
        return result.scalar_one()

    async def is_column_filled(self, user_id: int, *column_names: str) -> bool:
        user_exists = await self.exists(user_id=user_id)
        if not user_exists:
            return False

        query = select(
            *(
                getattr(OrderModel, column_name)
                for column_name in column_names
                if hasattr(OrderModel, column_name)
            )
        ).where(OrderModel.user_id == user_id)

        result = await self.session.execute(query)
        column_value = result.scalar_one_or_none()
        return column_value is not None

    async def _get(self, **kwargs: Optional[Any]) -> Optional[_OrderResult]:
        exists = await self.exists(**kwargs)
        if not exists:
            return None

        if kwargs:
            query = select(OrderModel).filter_by(**kwargs)
        else:
            query = select(OrderModel)

        result = await self.session.execute(query)
        return result

    async def get_one(self, **kwargs: Optional[Any]) -> Optional[Order]:
        res = await self._get(**kwargs)

        if res:
            db_order = res.scalar_one_or_none()
            return Order(
                id=db_order.id,
                user_id=db_order.user_id,
                product_id=db_order.product_id,
                status=db_order.status,
                price=db_order.price,
                time=db_order.time,
                name=db_order.name,
                additional_data=db_order.additional_data,
            )

    async def get_all(self, **kwargs: Optional[Any]) -> Optional[List[Order]]:
        res = await self._get(**kwargs)

        if res:
            db_orders = res.scalars().all()
            return [
                Order(
                    id=db_order.id,
                    user_id=db_order.user_id,
                    product_id=db_order.product_id,
                    status=db_order.status,
                    price=db_order.price,
                    time=db_order.time,
                    name=db_order.name,
                    additional_data=db_order.additional_data,
                )
                for db_order in db_orders
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(OrderModel).filter_by(**kwargs)
        await self.session.execute(query)
        await self.session.commit()
