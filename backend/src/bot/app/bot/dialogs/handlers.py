import uuid

from aiogram.types import CallbackQuery, Message
from aiogram import Bot

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Row, Back, Select
from aiogram_dialog.widgets.text import Format

from dishka import FromDishka

from src.bot.app.bot.states.product import ProductManagementSG
from .inject_wrappers import inject_on_click
from src.services import ProductService, YandexStorageClient, CategoryService


async def message_input_fixing(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
):
    dialog_manager.show_mode = ShowMode.NO_UPDATE


async def add_product(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.ADD_PRODUCT_NAME)


async def add_category(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.ADD_CATEGORY_NAME)


async def on_category_name(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["category_name"] = value
    await dialog_manager.switch_to(ProductManagementSG.ADD_CATEGORY_PHOTO)


@inject_on_click
async def hide_category(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    category_service: FromDishka[CategoryService],
):
    category_id = dialog_manager.dialog_data["category_id"]
    await category_service.update_category(category_id=int(category_id), is_visible=False)
    await dialog_manager.switch_to(ProductManagementSG.CATEGORY_MANAGEMENT)


@inject_on_click
async def show_category(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    category_service: FromDishka[CategoryService],
):
    category_id = dialog_manager.dialog_data["category_id"]
    await category_service.update_category(category_id=int(category_id), is_visible=True)
    await dialog_manager.switch_to(ProductManagementSG.CATEGORY_MANAGEMENT)


@inject_on_click
async def hide_product(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
):
    product_id = dialog_manager.dialog_data["product_id"]
    await product_service.update_product(product_id=product_id, is_visible=False)
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


@inject_on_click
async def show_product(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
):
    product_id = dialog_manager.dialog_data["product_id"]
    await product_service.update_product(product_id=product_id, is_visible=True)
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


@inject_on_click
async def disable_auto_delivery(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
) -> None:
    product_id = dialog_manager.dialog_data["product_id"]
    await product_service.update_product(product_id=product_id, is_auto_purchase=False, auto_purchase_text=None)
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


@inject_on_click
async def on_auto_purchase_text(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
    product_service: FromDishka[ProductService],
    yandex_storage_client: FromDishka[YandexStorageClient],
) -> None:
    product_id = dialog_manager.dialog_data["product_id"]
    bot = dialog_manager.middleware_data.get("bot")
    auto_purchase_image_url = None
    if message.photo:
        auto_purchase_file = await bot.get_file(message.photo[-1].file_id)
        auto_purchase_image_bytes = await bot.download_file(auto_purchase_file.file_path)
        auto_purchase_image_url = await yandex_storage_client.upload_file(auto_purchase_image_bytes, object_name=f"{message.photo[-1].file_id}.jpg")
    await product_service.update_product(product_id=product_id, auto_purchase_text=value, is_auto_purchase=True, auto_purchase_image_url=auto_purchase_image_url)
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


@inject_on_click
async def disable_purchase_limit(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
) -> None:
    product_id = dialog_manager.dialog_data["product_id"]
    await product_service.update_product(product_id=product_id, purchase_limit=None)
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


@inject_on_click
async def on_set_purchase_limit(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
    product_service: FromDishka[ProductService],
) -> None:
    await product_service.update_product(product_id=dialog_manager.dialog_data["product_id"], purchase_limit=int(value))
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


@inject_on_click
async def on_input_photo_new_category(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    yandex_storage_client: FromDishka[YandexStorageClient],
):
    bot = dialog_manager.middleware_data.get("bot")
    file = await bot.get_file(message.photo[-1].file_id)
    photo_bytes = await bot.download_file(file.file_path)
    
    image_url = await yandex_storage_client.upload_file(photo_bytes, object_name=f"{message.photo[-1].file_id}.jpg")
    dialog_manager.dialog_data["category_photo"] = image_url
    await dialog_manager.switch_to(ProductManagementSG.ADD_CATEGORY_THREAD_ID)


@inject_on_click
async def on_category_thread_id(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
    category_service: FromDishka[CategoryService],
):
    dialog_manager.dialog_data["category_thread_id"] = int(value)
    await category_service.add_category(
        game_id=int(dialog_manager.dialog_data["game_id"]),
        name=dialog_manager.dialog_data["category_name"],
        is_visible=True,
        image=dialog_manager.dialog_data["category_photo"],
        thread_id=int(dialog_manager.dialog_data["category_thread_id"]),
    )
    await dialog_manager.switch_to(ProductManagementSG.GAME_MANAGEMENT)


async def selected_category(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data["category_id"] = item_id
    await dialog_manager.switch_to(ProductManagementSG.CATEGORY_MANAGEMENT)


async def selected_game(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data["game_id"] = item_id
    await dialog_manager.switch_to(ProductManagementSG.GAME_MANAGEMENT)


async def selected_product(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data["product_id"] = item_id
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


@inject_on_click
async def delete_product(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
):
    await product_service.delete_product(product_id=dialog_manager.dialog_data["product_id"])
    await dialog_manager.switch_to(ProductManagementSG.GAME_MANAGEMENT)


async def back_to_product(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


async def back_to_game_management(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.GAME_MANAGEMENT)


async def edit_product_name(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.EDIT_PRODUCT_NAME)


async def edit_product_description(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.EDIT_PRODUCT_DESCRIPTION)


async def edit_product_instruction(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.EDIT_PRODUCT_INSTRUCTION)


async def edit_product_photo(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.EDIT_PRODUCT_PHOTO)


async def edit_product_price(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.EDIT_PRODUCT_PRICE)


@inject_on_click
async def on_product_name(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
    product_service: FromDishka[ProductService],
):  
    await product_service.update_product(
        product_id=dialog_manager.dialog_data["product_id"],
        name=value,
    )
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)
    await callback_query.answer("Название товара успешно изменено", show_alert=True)


@inject_on_click
async def on_product_description(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
    product_service: FromDishka[ProductService],
):  
    await product_service.update_product(
        product_id=dialog_manager.dialog_data["product_id"],
        description=value,
    )
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)
    await callback_query.answer("Описание товара успешно изменено", show_alert=True)


@inject_on_click
async def on_product_instruction(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
    yandex_storage_client: FromDishka[YandexStorageClient],
):  
    bot = dialog_manager.middleware_data.get("bot")
    instruction_image_url = None
    if message.photo:
        instruction_file = await bot.get_file(message.photo[-1].file_id)
        instruction_photo_bytes = await bot.download_file(instruction_file.file_path)
        instruction_image_url = await yandex_storage_client.upload_file(instruction_photo_bytes, object_name=f"{message.photo[-1].file_id}.jpg")
    await product_service.update_product(
        product_id=dialog_manager.dialog_data["product_id"],
        instruction=message.caption if message.caption else message.text,
        instruction_image_url=instruction_image_url,
    )
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)
    await message.delete()
    await message.answer("Инструкция товара успешно изменена", show_alert=True)


@inject_on_click
async def on_product_price(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
    product_service: FromDishka[ProductService],
):  
    await product_service.update_product(
        product_id=dialog_manager.dialog_data["product_id"],
        price=float(value),
    )
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)
    await callback_query.answer("Цена товара успешно изменена", show_alert=True)


@inject_on_click
async def on_input_photo(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
    yandex_storage_client: FromDishka[YandexStorageClient],
):  
    bot = dialog_manager.middleware_data.get("bot")
    file = await bot.get_file(message.photo[-1].file_id)
    photo_bytes = await bot.download_file(file.file_path)
    
    image_url = await yandex_storage_client.upload_file(photo_bytes, object_name=f"{message.photo[-1].file_id}.jpg")
    await product_service.update_product(
        product_id=dialog_manager.dialog_data["product_id"],
        image_url=image_url,
    )
    await message.delete()
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


async def on_product_name_new_product(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["product_name"] = value
    await dialog_manager.switch_to(ProductManagementSG.ADD_PRODUCT_DESCRIPTION)


async def on_product_description_new_product(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["product_description"] = value
    await dialog_manager.switch_to(ProductManagementSG.ADD_PRODUCT_INSTRUCTION)


async def on_product_instruction_new_product(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data["product_instruction_photo"] = message.photo[-1].file_id if message.photo else None
    dialog_manager.dialog_data["product_instruction"] = message.caption if message.caption else message.text
    await dialog_manager.switch_to(ProductManagementSG.ADD_PRODUCT_PRICE)


async def on_product_instruction_photo_new_product(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["product_instruction_photo"] = message.photo[-1].file_id
    await dialog_manager.switch_to(ProductManagementSG.ADD_PRODUCT_PRICE)


async def on_product_price_new_product(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["product_price"] = float(value)
    await dialog_manager.switch_to(ProductManagementSG.ADD_PRODUCT_PHOTO)


@inject_on_click
async def on_input_photo_new_product(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
    yandex_storage_client: FromDishka[YandexStorageClient],
):  
    bot = dialog_manager.middleware_data.get("bot")
    file = await bot.get_file(message.photo[-1].file_id)
    photo_bytes = await bot.download_file(file.file_path)

    games_dict = {
        "1": "Brawl Stars",
        "5": "Squad Busters",
        "2": "Clash of Clans",
        "3": "Clash Royale",
        "4": "Hay Day",
    }
    product_instruction_photo_file_id = dialog_manager.dialog_data.get("product_instruction_photo")
    instruction_image_url = None
    if product_instruction_photo_file_id:
        instruction_file = await bot.get_file(product_instruction_photo_file_id)
        instruction_photo_bytes = await bot.download_file(instruction_file.file_path)
        instruction_image_url = await yandex_storage_client.upload_file(instruction_photo_bytes, object_name=f"{product_instruction_photo_file_id}.jpg")
    image_url = await yandex_storage_client.upload_file(photo_bytes, object_name=f"{message.photo[-1].file_id}.jpg")
    await product_service.create_product(
        id=uuid.uuid4(),
        category_id=int(dialog_manager.dialog_data["category_id"]),
        name=dialog_manager.dialog_data["product_name"],
        description=dialog_manager.dialog_data["product_description"],
        instruction=dialog_manager.dialog_data["product_instruction"],
        price=int(dialog_manager.dialog_data["product_price"]),
        image_url=image_url,
        game_id=int(dialog_manager.dialog_data["game_id"]),
        game_name=games_dict[dialog_manager.dialog_data["game_id"]],
        instruction_image_url=instruction_image_url,
    )
    await message.delete()
    await dialog_manager.switch_to(ProductManagementSG.CATEGORY_MANAGEMENT)
