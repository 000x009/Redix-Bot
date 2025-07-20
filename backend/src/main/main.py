from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from redis import asyncio as aioredis

from src.main.ioc import Container
from src.api.http import (
    product,
    profile,
    promo,
    referral_system,
    supercell_auth,
    feedback,
    payment_system,
    game,
    category,
    cloud_storage,
    admin,
    stars,
)
from src.main.config import settings


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     redis = aioredis.from_url("redis://redis", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     yield
#     await redis.close()


app = FastAPI()
container = Container()
app.container = container

container.config.from_dict({
    "YANDEX_STORAGE_TOKEN": settings.YANDEX_STORAGE_TOKEN,
    "YANDEX_STORAGE_SECRET": settings.YANDEX_STORAGE_SECRET,
    "YANDEX_STORAGE_BUCKET_NAME": settings.YANDEX_STORAGE_BUCKET_NAME,
})
container.wire(modules=[__name__])

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://212.113.117.144:3000",
    "https://redixshop.com",
    "https://www.redixshop.com",
    "http://redixshop.com",
    "http://www.redixshop.com",
    "https://api.redixshop.com",
    "https://www.api.redixshop.com",
    "http://api.redixshop.com",
    "http://www.api.redixshop.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


app.include_router(product.router)
app.include_router(profile.router)
app.include_router(promo.router)
app.include_router(referral_system.router)
app.include_router(supercell_auth.router)
app.include_router(feedback.router)
app.include_router(payment_system.router)
app.include_router(game.router)
app.include_router(category.router)
app.include_router(cloud_storage.router)
app.include_router(admin.router)
app.include_router(stars.router)