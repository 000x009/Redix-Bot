from typing import Optional, Any, List

from src.data.dal import UserDAL
from src.schema import User


class UserService:
    def __init__(self, user_dal: UserDAL) -> None:
        self.__user_dal = user_dal

    async def get_users(self, **params: Optional[Any]) -> Optional[List[User]]:
        return await self.__user_dal.get_all(**params)
    
    async def get_one_user(self, **params: Optional[Any]) -> Optional[User]:
        return await self.__user_dal.get_one(**params)
    
    async def update_user(self, user_id: int, **values) -> None:
        await self.__user_dal.update(user_id=user_id, **values)

    async def add_user(self, **params) -> None:
        await self.__user_dal.add(**params)
    
    async def exists(self, **params) -> bool:
        return await self.__user_dal.exists(**params)
    
    async def get_new_users_amount(self) -> dict[str, int]:
        today = await self.__user_dal.get_new_users_amount(1)
        week = await self.__user_dal.get_new_users_amount(7)
        month = await self.__user_dal.get_new_users_amount(30)
        all_time = await self.__user_dal.get_new_users_amount()

        return {
            "today": today,
            "week": week,
            "month": month,
            "all_time": all_time
        }
