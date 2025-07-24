from aiogram import F

from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Button,
    ScrollingGroup,
    Select,
    Back,
    PrevPage,
    CurrentPage,
    NextPage,
    Row,
    SwitchTo
)
from aiogram_dialog.widgets.text import Format, Const

from app.bot.states.admin import AdminManagementSG
from .handlers import message_input_fixing
from .admin_handlers import (
    selected_admin,
    remove_admin,
    on_new_admin_user_id,
    switch_mailing_permission,
    switch_products_permission,
    switch_users_permission,
    switch_promos_permission,
    switch_statistics_permission,
    switch_admins_permission,
    switch_stars_permission,
)
from .admin_getter import admins_getter, one_admin_getter



async def close_dialog(_, __, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.done()


admin_management_dialog = Dialog(
    Window(
        Const("Список администраторов", when=F['admins']),
        Const("Список администраторов пуст", when=~F['admins']),
        ScrollingGroup(
            Select(
                id="admin_select",
                items="admins",
                item_id_getter=lambda item: item.user_id,
                text=Format("{item.user_id}"),
                on_click=selected_admin,
            ),
            id="admin_group",
            height=10,
            width=2,
            hide_on_single_page=True,
            hide_pager=True,
            when=F['admins']
        ),
        Row(
            PrevPage(
                scroll="admin_group", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="admin_group", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="admin_group", text=Format("▶️"),
            ),
            when=F['admins']
        ),
        SwitchTo(
            id='add_admin',
            text=Format("Добавить администратора"),
            state=AdminManagementSG.ADD_ADMIN,
        ),
        MessageInput(
            func=message_input_fixing
        ),
        state=AdminManagementSG.ADMIN_LIST,
        getter=admins_getter,
    ),
    Window(
        Format("Администратор: {admin.user_id}\nРоль: {admin.role.value}"),
        Button(
            id="mailing_permission",
            text=Format("🔴 Рассылка", when=~F['permissions']['mailing']),
            on_click=switch_mailing_permission,
        ),
        Button(
            id="mailing_permission",
            text=Format("🟢 Рассылка", when=F['permissions']['mailing']),
            on_click=switch_mailing_permission,
        ),
        Button(
            id="products_permission",
            text=Format("🔴 Управление товарами", when=~F['permissions']['products']),
            on_click=switch_products_permission,
        ),
        Button(
            id="products_permission",
            text=Format("🟢 Управление товарами", when=F['permissions']['products']),
            on_click=switch_products_permission,
        ),
        Button(
            id="users_permission",
            text=Format("🔴 Управление пользователями", when=~F['permissions']['users']),
            on_click=switch_users_permission,
        ),
        Button(
            id="users_permission",
            text=Format("🟢 Управление пользователями", when=F['permissions']['users']),
            on_click=switch_users_permission,
        ),
        Button(
            id="promos_permission",
            text=Format("🔴 Управление промокодами", when=~F['permissions']['promos']),
            on_click=switch_promos_permission,
        ),
        Button(
            id="promos_permission",
            text=Format("🟢 Управление промокодами", when=F['permissions']['promos']),
            on_click=switch_promos_permission,
        ),
        Button(
            id="statistics_permission",
            text=Format("🔴 Управление статистикой", when=~F['permissions']['statistics']),
            on_click=switch_statistics_permission,
        ),
        Button(
            id="statistics_permission",
            text=Format("🟢 Управление статистикой", when=F['permissions']['statistics']),
            on_click=switch_statistics_permission,
        ),
        Button(
            id="admins_permission",
            text=Format("🔴 Управление администраторами", when=~F['permissions']['admins']),
            on_click=switch_admins_permission,
        ),
        Button(
            id="admins_permission",
            text=Format("🟢 Управление администраторами", when=F['permissions']['admins']),
            on_click=switch_admins_permission,
        ),
        Button(
            id="stars_permission",
            text=Format("🔴 Управление звездами", when=~F['permissions']['stars']),
            on_click=switch_stars_permission,
        ),
        Button(
            id="stars_permission",
            text=Format("🟢 Управление звездами", when=F['permissions']['stars']),
            on_click=switch_stars_permission,
        ),
        Button(
            id='remove_admin',
            text=Format("Снять админа"),
            on_click=remove_admin,
        ),
        MessageInput(
            func=message_input_fixing
        ),
        Back(Format("◀️ Назад")),
        state=AdminManagementSG.ADMIN_INFO,
        getter=one_admin_getter,
    ),
    Window(
        Const("Введите ID пользователя, которого желаете добавить в администраторы"),
        TextInput(
            id="add_admin_user_id",
            on_success=on_new_admin_user_id,
        ),
        state=AdminManagementSG.ADD_ADMIN,
    ),
    on_process_result=close_dialog,
)
