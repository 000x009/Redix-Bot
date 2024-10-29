from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dependency_injector.wiring import inject, Provide

from src.main.ioc import Container
from src.services import SupercellAuthService, SupercellClient
from src.api.schema.supercell import SupercellAuthDTO, VerifyTagSchema


router = APIRouter(
    prefix="/supercell",
    tags=["Supercell Auth"],
)


@router.post("/login")
@inject
async def login(
    data: SupercellAuthDTO,
    supercell_service: SupercellAuthService = Depends(Provide[Container.supercell_service]),
) -> JSONResponse:
    supercell_service.login(email=data.email, game=data.game)
    
    return JSONResponse(status_code=200, content=dict(message='success'))


@router.post("/verify-tag")
@inject
async def verify_tag(
    data: VerifyTagSchema,
    supercell_client: SupercellClient = Depends(Provide[Container.supercell_client]),
) -> JSONResponse:
    exists = await supercell_client.verify_tag(data.tag)
    return JSONResponse(status_code=200, content=dict(exists=exists))
