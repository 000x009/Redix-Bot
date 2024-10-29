from typing import List

from fastapi import APIRouter, Depends

from dependency_injector.wiring import inject, Provide

from src.main.ioc import Container
from src.services import GameService
from src.schema.game import Game

router = APIRouter(
    prefix="/games",
    tags=["Games"],
)


@router.get("/")
@inject
async def get_all_games(
    game_service: GameService = Depends(Provide[Container.game_service]),
) -> List[Game]:
    response = await game_service.get_all_games()

    return response


@router.get("/{game_id}")
@inject
async def get_game(
    game_id: int,
    game_service: GameService = Depends(Provide[Container.game_service]),
) -> Game:
    response = await game_service.get_game(id=game_id)
    
    return response
