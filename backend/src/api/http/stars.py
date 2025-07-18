from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dependency_injector.wiring import inject, Provide

from src.main.ioc import Container
from src.services import FragmentAPI
from src.data.dal import StarsDAL

class BuyStarsDTO(BaseModel):
    username: str
    quantity: int


router = APIRouter(
    prefix="/stars",
    tags=["Stars"],
)


@router.post("/buy-stars")
@inject
async def buy_stars(
    data: BuyStarsDTO,
    stars_dal: StarsDAL = Depends(Provide[Container.stars_dal]),
    fragment_service: FragmentAPI = Depends(Provide[Container.fragment_service]),
) -> JSONResponse:
    stars_config = await stars_dal.get_one()
    if not stars_config:
        return JSONResponse(status_code=400, content=dict(message='Stars config not found'))
    
    fragment_service.set_hash_and_cookie(stars_config.api_hash, stars_config.api_cookie, stars_config.mnemonic)
    await fragment_service.buy_stars(data.username, data.quantity)

    return JSONResponse(status_code=200, content=dict(message='success'))


@router.get("/rate")
@inject
async def get_stars_rate(
    stars_dal: StarsDAL = Depends(Provide[Container.stars_dal]),
) -> JSONResponse:
    stars_config = await stars_dal.get_one()
    if not stars_config:
        return JSONResponse(status_code=400, content=dict(message='Stars rates not found'))
    return JSONResponse(status_code=200, content=dict(rate=stars_config.rate))
