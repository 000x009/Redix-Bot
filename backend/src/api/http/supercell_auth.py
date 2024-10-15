from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from src.services import SupercellAuthService
from src.api.schema.supercell import SupercellAuthDTO


router = APIRouter(
    prefix="/supercell",
    tags=["Supercell Auth"],
    route_class=DishkaRoute
)


@router.post("/login")
async def login(
    data: SupercellAuthDTO,
    supercell_service: FromDishka[SupercellAuthService],
) -> JSONResponse:
    supercell_service.login(email=data.email, game=data.game)
    
    return JSONResponse(status_code=200, content=dict(message='success'))
