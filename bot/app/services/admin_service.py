from typing import List, Optional, Any

from app.data.dal import AdminDAL
from app.schema.admin import Admin


class AdminService:
    def __init__(self, dal: AdminDAL) -> None:
        self.dal = dal
    
    async def add(self, **kwargs) -> None:
        await self.dal.add(**kwargs)

    async def update(self, user_id: int, **kwargs) -> None:
        await self.dal.update(user_id, **kwargs)

    async def get(self, **kwargs) -> Optional[Admin]:
        return await self.dal.get(**kwargs)

    async def get_all(self, **kwargs: Optional[Any]) -> Optional[List[Admin]]:
        return await self.dal.get_all(**kwargs)

    async def delete(self, **kwargs) -> None:
        await self.dal.delete(**kwargs)

