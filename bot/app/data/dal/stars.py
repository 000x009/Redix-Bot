from decimal import Decimal
from dataclasses import dataclass
from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, Result, insert

from app.data.models import StarsModel


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

    async def get_one(self, **kwargs: Optional[Any]) -> Optional[Stars]:
        query = select(StarsModel).filter_by(**kwargs)
        result = await self.session.execute(query)
        db_stars = result.scalars().first()

        if not db_stars:
            return None

        return Stars(
            rate=db_stars.rate,
            api_hash=db_stars.api_hash,
            api_cookie=db_stars.api_cookie,
            mnemonic=db_stars.mnemonic.split('|'),
        )

    async def add(self, **kwargs) -> None:
        query = insert(StarsModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()
