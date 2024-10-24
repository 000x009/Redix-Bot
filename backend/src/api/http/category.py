from typing import List

from fastapi import APIRouter

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from src.services import CategoryService
from src.schema import Category

router = APIRouter(
    prefix="/category",
    tags=["Category"],
    route_class=DishkaRoute,
)


@router.get("/")
async def get_categories(
    game_id: int,
    category_service: FromDishka[CategoryService],
) -> List[Category]:
    return await category_service.get_categories(game_id=game_id, is_visible=True)


@router.get("/{id}")
async def get_one_category(
    id: int,
    category_service: FromDishka[CategoryService],
) -> Category:
    return await category_service.get_category(id=id)
 