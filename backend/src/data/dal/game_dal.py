from typing import Optional, TypeAlias, List, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result, func

from src.schema.game import Game
from src.data.models import GameModel


_ProductResult: TypeAlias = Result[tuple[GameModel]]


class GameDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(GameModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, product_id: UUID, **kwargs) -> None:
        query = update(GameModel).where(GameModel.id == product_id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, **kwargs: Optional[Any]) -> bool:
        query = select(exists(GameModel))
        if kwargs:
            query = select(
                exists().where(
                    *(
                        getattr(GameModel, key) == value
                        for key, value in kwargs.items()
                        if hasattr(GameModel, key)
                    )
                )
            )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def is_column_filled(self, id: int, *column_names: str) -> bool:
        user_exists = await self.exists(id=id)
        if not user_exists:
            return False

        query = select(
            *(
                getattr(GameModel, column_name)
                for column_name in column_names
                if hasattr(GameModel, column_name)
            )
        ).where(GameModel.id == id)

        result = await self.session.execute(query)
        column_value = result.scalar_one_or_none()
        return column_value is not None

    async def _get(self, **kwargs: Optional[Any]) -> Optional[_ProductResult]:
        exists = await self.exists(**kwargs)
        if not exists:
            return None

        query = select(GameModel).order_by(GameModel.web_app_place)
        if kwargs:
            query = select(GameModel).filter_by(**kwargs).order_by(GameModel.web_app_place)

        result = await self.session.execute(query)
        return result

    async def get_one(self, **kwargs: Optional[Any]) -> Optional[Game]:
        query = select(GameModel).filter_by(**kwargs)
        result = await self.session.execute(query)

        if result:
            db_game = result.scalar_one_or_none()
            return Game(
                id=db_game.id,
                name=db_game.name,
                image_url=db_game.image_url,
            )

    async def get_all(self, **kwargs: Optional[Any]) -> Optional[List[Game]]:
        res = await self._get(**kwargs)

        if res:
            db_games = res.scalars().all()
            return [
                Game(
                    id=db_game.id,
                    name=db_game.name,
                    image_url=db_game.image_url
                )
                for db_game in db_games
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(GameModel).filter_by(**kwargs)
        await self.session.execute(query)
        await self.session.commit()
