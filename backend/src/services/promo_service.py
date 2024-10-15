import uuid
from typing import Optional, Any, List

from src.data.dal import PromoDAL
from src.schema import Promo


class PromoService:
    def __init__(self, promo_dal: PromoDAL) -> None:
        self.__promo_dal = promo_dal

    async def get_promos(self, **params: Optional[Any]) -> Optional[List[Promo]]:
        return await self.__promo_dal.get_all(**params)
    
    async def get_one_promo(self, **params: Optional[Any]) -> Optional[Promo]:
        return await self.__promo_dal.get_one(**params)

    async def add_promo(self, **params: Optional[Any]) -> Optional[Promo]:
        return await self.__promo_dal.add(**params)

    async def update_promo(
        self,
        promo_id: Optional[uuid.UUID] = None,
        name: Optional[str] = None,
        **values,
    ) -> None:
        await self.__promo_dal.update(promo_id=promo_id, name=name, **values)
        
    async def delete_promo(self, **params: Optional[Any]) -> None:
        await self.__promo_dal.delete(**params)