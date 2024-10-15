from typing import Optional, TypeAlias, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result

from src.schema import User
from src.data.models import UserModel


_UserResult: TypeAlias = Result[tuple[UserModel]]


class UserDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(UserModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, user_id: int, **kwargs) -> None:
        query = update(UserModel).where(UserModel.user_id == user_id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, **kwargs) -> bool:
        query = select(
            exists().where(
                *(
                    getattr(UserModel, key) == value
                    for key, value in kwargs.items()
                    if hasattr(UserModel, key)
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def is_column_filled(self, user_id: int, *column_names: str) -> bool:
        user_exists = await self.exists(user_id=user_id)
        if not user_exists:
            return False

        query = select(
            *(
                getattr(UserModel, column_name)
                for column_name in column_names
                if hasattr(UserModel, column_name)
            )
        ).where(UserModel.user_id == user_id)

        result = await self.session.execute(query)
        column_value = result.scalar_one_or_none()
        return column_value is not None

    async def _get(self, **kwargs) -> Optional[_UserResult]:
        query = select(UserModel)
        if kwargs:
            exists = await self.exists(**kwargs)
            if not exists:
                return None
            query = select(UserModel).filter_by(**kwargs)
    
        result = await self.session.execute(query)
        return result

    async def get_one(self, **kwargs) -> Optional[User]:
        res = await self._get(**kwargs)

        if res:
            db_user = res.scalar_one_or_none()
            return User(
                user_id=db_user.user_id,
                referral_code=db_user.referral_code,
                referral_id=db_user.referral_id,
                balance=db_user.balance,
                used_coupons=db_user.used_coupons,
                nickname=db_user.nickname,
                profile_photo=db_user.profile_photo,
            )

    async def get_all(self, **kwargs) -> Optional[List[User]]:
        res = await self._get(**kwargs)

        if res:
            db_users = res.scalars().all()
            return [
                User(
                    user_id=db_user.user_id,
                    referral_code=db_user.referral_code,
                    referral_id=db_user.referral_id,
                    balance=db_user.balance,
                    used_coupons=db_user.used_coupons,
                    nickname=db_user.nickname,
                    profile_photo=db_user.profile_photo,
                )
                for db_user in db_users
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(UserModel).filter_by(**kwargs)
        await self.session.execute(query)
        await self.session.commit()
