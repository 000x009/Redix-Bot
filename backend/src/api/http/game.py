from typing import List

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from src.services import GameService
from src.schema.game import Game

router = APIRouter(
    prefix="/games",
    tags=["Games"],
    route_class=DishkaRoute,
)


@router.get("/")
# @cache(expire=60 * 60 * 24)
async def get_all_games(
    game_service: FromDishka[GameService],
) -> List[Game]:
    response = await game_service.get_all_games()

    return response


@router.get("/{game_id}")
@cache(expire=60 * 60 * 24)
async def get_game(
    game_id: int,
    game_service: FromDishka[GameService],
) -> Game:
    response = await game_service.get_game(id=game_id)
    
    return response
