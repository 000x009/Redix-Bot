from decimal import Decimal
from dataclasses import dataclass
from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, Result

from src.data.models import StarsModel


@dataclass
class Stars:
    rate: Decimal
    api_hash: str
    api_cookie: str
    mnemonic: list[str]

_StarsResult = Result[tuple[StarsModel]]


class StarsDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def update(self, **kwargs) -> None:
        query = update(StarsModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def _get(self, **kwargs: Optional[Any]) -> Optional[_StarsResult]:
        if kwargs:
            query = select(StarsModel).filter_by(**kwargs)
        else:
            query = select(StarsModel)

        result = await self.session.execute(query)
        return result

    async def get_one(self, **kwargs: Optional[Any]) -> Optional[Stars]:
        res = await self._get(**kwargs)
        db_stars = res.scalar_one_or_none() if res else None

        if db_stars:
            return Stars(
                rate=db_stars.rate,
                api_hash=db_stars.api_hash,
                api_cookie=db_stars.api_cookie,
                mnemonic=db_stars.mnemonic.split('|'),
            )

        return None
