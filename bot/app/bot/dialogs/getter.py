from typing import Coroutine, Any
import uuid

from aiogram import Bot
from aiogram.types import InputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.manager.message_manager import MessageManager
from aiogram_dialog.api.entities import MediaAttachment

from aiogram.types import BufferedInputFile
from aiogram.enums import ContentType

from dishka import FromDishka

from app.services import GameService, ProductService, YandexStorageClient, CategoryService
from app.main.config import settings
from .inject_wrappers import inject_getter


class YandexStorageMedia(MessageManager):
    async def get_media_source(self, media: MediaAttachment, bot: Bot) -> Coroutine[Any, Any, InputFile | str]:
        yandex_storage_client = YandexStorageClient(
            token=settings.YANDEX_STORAGE_TOKEN,
            bucket_name=settings.YANDEX_STORAGE_BUCKET_NAME,
            secret=settings.YANDEX_STORAGE_SECRET,
        )

        if media.file_id:
            return await super().get_media_source(media, bot)
        if media.url:
            object_name = media.url.split('/')[-1]
            file = yandex_storage_client.get_file(object_url=media.url)
            return BufferedInputFile(file, filename=object_name)
        return await super().get_media_source(media, bot)


@inject_getter
async def games_getter(
    dialog_manager: DialogManager,
    game_service: FromDishka[GameService],
    **kwargs
) -> dict:
    games = await game_service.get_all_games()
    
    return {
        "games": games,
    }


@inject_getter
async def one_game_getter(
    dialog_manager: DialogManager,
    game_service: FromDishka[GameService],
    category_service: FromDishka[CategoryService],
    **kwargs,
) -> dict:
    game_id = dialog_manager.dialog_data["game_id"]
    game = await game_service.get_game(id=int(game_id))
    categories = await category_service.get_categories(game_id=int(game_id))

    return {
        "game": game,
        "categories": categories,
    }


@inject_getter
async def one_category_getter(
    dialog_manager: DialogManager,
    category_service: FromDishka[CategoryService],
    product_service: FromDishka[ProductService],
    **kwargs,
) -> dict:
    category_id = dialog_manager.dialog_data["category_id"]
    category = await category_service.get_category(id=category_id)
    products = await product_service.get_products(category_id=category_id)

    return {
        "category": category,
        "products": products,
    }


@inject_getter
async def one_product_getter(
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
    **kwargs,
) -> dict:
    yandex_storage_client = YandexStorageClient(
        token=settings.YANDEX_STORAGE_TOKEN,
        bucket_name=settings.YANDEX_STORAGE_BUCKET_NAME,
        secret=settings.YANDEX_STORAGE_SECRET,
    )
    product_id = dialog_manager.dialog_data["product_id"]
    product = await product_service.get_one_product(id=uuid.UUID(product_id))
    file = yandex_storage_client.get_file(object_url=product.image_url)

    return {
        "photo": MediaAttachment(
           url=product.image_url,
           type=ContentType.PHOTO,
        ) if file else None,
        "product": product,
    }


async def mailing_getter(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict:
    message = dialog_manager.start_data.get("message")
    album_caption = dialog_manager.start_data.get("album_caption")

    print("START DATA", dialog_manager.start_data)

    print(album_caption, flush=True)

    return {
        'message': message if message else album_caption,
    }
