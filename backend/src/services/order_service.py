from typing import Optional, Any, List
from uuid import UUID

from src.data.dal import OrderDAL
from src.schema import Order


class OrderService:
    def __init__(self, order_dal: OrderDAL) -> None:
        self.__order_dal = order_dal

    async def get_orders(self, **params: Optional[Any]) -> Optional[List[Order]]:
        return await self.__order_dal.get_all(**params)
    
    async def get_one_order(self, **params: Optional[Any]) -> Optional[Order]:
        return await self.__order_dal.get_one(**params)

    async def add_order(self, **params: Optional[Any]) -> None:
        return await self.__order_dal.add(**params)
    
    async def update_order(self, order_id: UUID, **params: Optional[Any]) -> None:
        return await self.__order_dal.update(order_id=order_id, **params)
    