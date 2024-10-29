from typing import List

from fastapi import APIRouter, Depends

from dependency_injector.wiring import inject, Provide

from src.main.ioc import Container
from src.services import CategoryService
from src.schema import Category

router = APIRouter(
    prefix="/category",
    tags=["Category"],
)


@router.get("/")
@inject
async def get_categories(
    game_id: int,
    category_service: CategoryService = Depends(Provide[Container.category_service]),
) -> List[Category]:
    response = await category_service.get_categories(game_id=game_id, is_visible=True)
    return response


@router.get("/{id}")
@inject
async def get_one_category(
    id: int,
    category_service: CategoryService = Depends(Provide[Container.category_service]),
) -> Category:
    return await category_service.get_category(id=id)
 