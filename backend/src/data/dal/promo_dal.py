import uuid
from typing import Optional, List, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result

from src.schema import Promo
from src.data.models import PromoModel


_PromoResult = Result[tuple[PromoModel]]


class PromoDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(PromoModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(
        self,
        promo_id: Optional[uuid.UUID] = None,
        name: Optional[str] = None,
        **kwargs,
    ) -> None:
        if promo_id:
            query = update(PromoModel).where(PromoModel.id == promo_id).values(**kwargs)
        else:
            query = update(PromoModel).where(PromoModel.name == name).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, **kwargs: Optional[Any]) -> bool:
        if kwargs:
            query = select(
                exists().where(
                    *(
                        getattr(PromoModel, key) == value
                        for key, value in kwargs.items()
                        if hasattr(PromoModel, key)
                    )
                )
            )
        query = select(exists(PromoModel))
        result = await self.session.execute(query)
        return result.scalar_one()

    async def is_column_filled(self, promo_id: int, *column_names: str) -> bool:
        user_exists = await self.exists(promo_id=promo_id)
        if not user_exists:
            return False

        query = select(
            *(
                getattr(PromoModel, column_name)
                for column_name in column_names
                if hasattr(PromoModel, column_name)
            )
        ).where(PromoModel.promo_id == promo_id)

        result = await self.session.execute(query)
        column_value = result.scalar_one_or_none()
        return column_value is not None

    async def _get(self, **kwargs: Optional[Any]) -> Optional[_PromoResult]:
        exists = await self.exists(**kwargs)
        if not exists:
            return None

        if kwargs:
            query = select(PromoModel).filter_by(**kwargs)
        query = select(PromoModel)

        result = await self.session.execute(query)
        return result

    async def get_one(self, **kwargs: Optional[Any]) -> Optional[Promo]:
        query = select(PromoModel).filter_by(**kwargs)
        result = await self.session.execute(query)
        db_promo = result.scalar_one_or_none()
        if db_promo:
            return Promo(
                id=db_promo.id,
                name=db_promo.name,
                bonus_amount=db_promo.bonus_amount,
                uses=db_promo.uses,
                status=db_promo.status,
            )
        return None

    async def get_all(self, **kwargs: Optional[Any]) -> Optional[List[Promo]]:
        res = await self._get(**kwargs)

        if res:
            db_promos = res.scalars().all()
            return [
                Promo(
                    id=db_promo.id,
                    name=db_promo.name,
                    bonus_amount=db_promo.bonus_amount,
                    uses=db_promo.uses,
                    status=db_promo.status,
                )
                for db_promo in db_promos
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(PromoModel).filter_by(**kwargs)
        await self.session.execute(query)
        await self.session.commit()
