from typing import Optional, List, Any
from uuid import UUID

from src.data.dal import ProductDAL
from src.schema import Product


class ProductService:
    def __init__(self, product_dal: ProductDAL) -> None:
        self.__product_dal = product_dal

    async def get_products(self, **params: Optional[Any]) -> Optional[List[Product]]:
        return await self.__product_dal.get_all(**params)
    
    async def get_one_product(self, **params: Optional[Any]) -> Optional[Product]:
        return await self.__product_dal.get_one(**params)
    
    async def create_product(self, **params) -> None:
        await self.__product_dal.add(**params)
    
    async def update_product(self, product_id: UUID, **params) -> None:
        await self.__product_dal.update(product_id=product_id, **params)

    async def search(self, search_name: str) -> List[Product]:
        return await self.__product_dal.search(search_name)

    async def delete_product(self, product_id: UUID) -> None:
        await self.__product_dal.delete(id=product_id)

