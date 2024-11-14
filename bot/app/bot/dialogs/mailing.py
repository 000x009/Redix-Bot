from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, PrevPage, CurrentPage, NextPage, Row, Button
from aiogram_dialog.widgets.text import Format, Const

from app.bot.states.mailing import MailingSG
from .getter import games_getter
from .handlers import (
    selected_game_button,
    message_input_fixing,
    main_menu_button,
    confirm_mailing,
    cancel_mailing,
)


async def close_dialog(_, __, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.done()


mailing_dialog = Dialog(
    Window(
        Const("Выберите кнопку"),
        ScrollingGroup(
            Select(
                id="game_select",
                items="games",
                item_id_getter=lambda item: item.id,
                text=Format("{item.name}"),
                on_click=selected_game_button,
            ),
            id="game_group",
            height=10,
            width=2,
            hide_on_single_page=True,
            hide_pager=True
        ),
        Button(
            id='main_menu_button',
            text=Const("Главное меню"),
            on_click=main_menu_button,
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
        state=MailingSG.BUTTON,
        getter=games_getter,
    ),
    Window(
        Const("Вы уверены, что хотите разослать это сообщение всем?"),
        Button(
            id='confirm_mailing_button',
            text=Const("✅ Да"),
            on_click=confirm_mailing,
        ),
        Button(
            id='cancel_mailing_button',
            text=Const("❌ Нет"),
            on_click=cancel_mailing,
        ),
        state=MailingSG.CHECKOUT,
    ),
    on_process_result=close_dialog,
)
