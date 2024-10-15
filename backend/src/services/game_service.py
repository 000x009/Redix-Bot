from typing import List, Optional, Any

from src.data.dal import GameDAL
from src.schema.game import Game


class GameService:
    def __init__(self, game_dal: GameDAL) -> None:
        self.game_dal = game_dal

    async def get_all_games(self, **kwargs: Optional[Any]) -> List[Game]:
        return await self.game_dal.get_all(**kwargs)

    async def get_game(self, **kwargs) -> Game:
        return await self.game_dal.get_one(**kwargs)

    async def create_game(self, **kwargs) -> None:
        return await self.game_dal.add(**kwargs)
