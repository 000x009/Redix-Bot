from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, Back, PrevPage, CurrentPage, NextPage, Row
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import DynamicMedia

from aiogram.enums.content_type import ContentType

from src.bot.app.bot.states.product import ProductManagementSG
from .getter import games_getter, one_game_getter, one_product_getter
from .handlers import (
    selected_game,
    selected_product,
    add_product,
    edit_product_name,
    edit_product_description,
    edit_product_instruction,
    edit_product_price,
    edit_product_photo,
    delete_product,
    on_product_name,
    on_product_description,
    on_product_instruction,
    on_product_price,
    on_input_photo,
    back_to_product,
    on_input_photo_new_product,
    back_to_game_management,
    on_product_name_new_product,
    on_product_description_new_product,
    on_product_instruction_new_product,
    on_product_price_new_product,
    message_input_fixing,
)


async def close_dialog(_, __, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.done()


product_management_dialog = Dialog(
    Window(
        Const("🎮 Список игр"),
        ScrollingGroup(
            Select(
                id="game_select",
                items="games",
                item_id_getter=lambda item: item.id,
                text=Format("{item.name}"),
                on_click=selected_game,
            ),
            id="game_group",
            height=10,
            width=2,
            hide_on_single_page=True,
            hide_pager=True
        ),
        Row(
            PrevPage(
                scroll="game_group", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="game_group", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="game_group", text=Format("▶️"),
            ),
        ),
        MessageInput(
            func=message_input_fixing
        ),
        state=ProductManagementSG.GAMES,
        getter=games_getter,
    ),
    Window(
        Format("Игра: {game.name}"),
        ScrollingGroup(
            Select(
                id="product_select",
                items="products",
                item_id_getter=lambda item: item.id,
                text=Format("🔴 | {item.name}"),
                on_click=selected_product,
            ),
            id="product_group",
            height=10,
            width=2,
            hide_on_single_page=True,
            hide_pager=True,
            when="products"
        ),
        Button(
            id='add_product',
            text=Format("Добавить товар"),
            on_click=add_product,
        ),
        Row(
            PrevPage(
                scroll="product_group", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="product_group", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="product_group", text=Format("▶️"),
            ),
            when="products"
        ),
        MessageInput(
            func=message_input_fixing
        ),
        Back(Format("◀️ Назад")),
        state=ProductManagementSG.GAME_MANAGEMENT,
        getter=one_game_getter,
    ),
    Window(
        DynamicMedia(selector="photo"),
        Const("Выберите изменение"),
        Row(
            Button(
                id="edit_product_name",
                text=Format("Название"),
                on_click=edit_product_name,
            ),
            Button(
                id="edit_product_photo",
                text=Format("Фото"),
                on_click=edit_product_photo,
            ),
        ),
        Row(
            Button(
                id="edit_product_description",
                text=Format("Описание"),
                on_click=edit_product_description,
            ),
            Button(
                id="edit_product_instruction",
                text=Format("Инструкция"),
                on_click=edit_product_instruction,
            ),
        ),
        Row(
            Button(
                id="edit_product_price",
                text=Format("Цена"),
                on_click=edit_product_price,
            ),
        ),
        Button(
            id="delete_product",
            text=Format("🗑️ Удалить товар"),
            on_click=delete_product,
        ),
        Back(Format("◀️ Назад")),
        MessageInput(
            func=message_input_fixing
        ),
        state=ProductManagementSG.PRODUCT,
        getter=one_product_getter,
    ),
    Window(
        Const("Введите новое название товара"),
        TextInput(
            id="edit_product_name_text",
            on_success=on_product_name,
        ),
        Back(Format("◀️ Назад")),
        state=ProductManagementSG.EDIT_PRODUCT_NAME,
    ),
    Window(
        Const("Введите новое описание товара"),
        TextInput(
            id="edit_product_description_text",
            on_success=on_product_description,
        ),
        Back(Format("◀️ Назад"), on_click=back_to_product),
        state=ProductManagementSG.EDIT_PRODUCT_DESCRIPTION,
    ),
    Window(
        Const("Введите новую инструкцию товара"),
        TextInput(
            id="edit_product_instruction_text",
            on_success=on_product_instruction,
        ),
        Back(Format("◀️ Назад"), on_click=back_to_product),
        state=ProductManagementSG.EDIT_PRODUCT_INSTRUCTION,
    ),
    Window(
        Const("Введите новую цену товара"),
        TextInput(
            id="edit_product_price_text",
            on_success=on_product_price,
        ),
        Back(Format("◀️ Назад"), on_click=back_to_product),
        state=ProductManagementSG.EDIT_PRODUCT_PRICE,
    ),
    Window(
        Const("Отправьте новое фото товара"),
        MessageInput(on_input_photo, content_types=[ContentType.PHOTO]),
        Back(Format("◀️ Назад"), on_click=back_to_product),
        state=ProductManagementSG.EDIT_PRODUCT_PHOTO,
    ),
    Window(
        Const("Введите название нового товара"),
        TextInput(
            id="add_product_name_text",
            on_success=on_product_name_new_product,
        ),
        Back(Format("◀️ Назад"), on_click=back_to_game_management),
        state=ProductManagementSG.ADD_PRODUCT_NAME,
    ),
    Window(
        Const("Введите описание нового товара"),
        TextInput(
            id="add_product_description_text",
            on_success=on_product_description_new_product,
        ),
        state=ProductManagementSG.ADD_PRODUCT_DESCRIPTION,
    ),
    Window(
        Const("Введите инструкцию нового товара"),
        TextInput(
            id="add_product_instruction_text",
            on_success=on_product_instruction_new_product,
        ),
        state=ProductManagementSG.ADD_PRODUCT_INSTRUCTION,
    ),
    Window(
        Const("Введите цену нового товара"),
        TextInput(
            id="add_product_price_text",
            on_success=on_product_price_new_product,
        ),
        state=ProductManagementSG.ADD_PRODUCT_PRICE,
    ),
    Window(
        Const("Отправьте фото нового товара"),
        MessageInput(on_input_photo_new_product, content_types=[ContentType.PHOTO]),
        state=ProductManagementSG.ADD_PRODUCT_PHOTO,
    ),
    on_process_result=close_dialog,
)
