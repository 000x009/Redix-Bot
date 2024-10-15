from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from src.api.http import (
    product,
    profile,
    promo,
    referral_system,
    supercell_auth,
    feedback,
    payment_system,
    game,
)
from src.main.ioc import DALProvider, DatabaseProvider, ServiceProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://redis", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://62.76.233.156:3000",
    "https://paradox-shop.ru",
    "https://www.paradox-shop.ru",
    "http://paradox-shop.ru",
    "http://www.paradox-shop.ru",
    "https://api.paradox-shop.ru",
    "https://www.api.paradox-shop.ru",
    "http://api.paradox-shop.ru",
    "http://www.api.paradox-shop.ru",
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


# @app.exception_handler(DBAPIError)
# async def validation_exception_handler(request: Request, exc: DBAPIError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": "Wrong SQL statement or params."}),
#     )


app.include_router(product.router)
app.include_router(profile.router)
app.include_router(promo.router)
app.include_router(referral_system.router)
app.include_router(supercell_auth.router)
app.include_router(feedback.router)
app.include_router(payment_system.router)
app.include_router(game.router)

container = make_async_container(DALProvider(), DatabaseProvider(), ServiceProvider())
setup_dishka(container, app)
