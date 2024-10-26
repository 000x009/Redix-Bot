from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import ShowMode
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.input import TextInput

from dishka import FromDishka

from src.services import AdminService
from src.bot.app.bot.states.admin import AdminManagementSG
from .inject_wrappers import inject_on_click, inject_on_process_result
from src.data.models.admin import AdminRole


async def selected_admin(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data["admin_user_id"] = item_id
    await dialog_manager.switch_to(AdminManagementSG.ADMIN_INFO)


@inject_on_click
async def remove_admin(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    admin_service: FromDishka[AdminService],
) -> None:
    await admin_service.delete(user_id=int(dialog_manager.dialog_data["admin_user_id"]))
    await callback_query.answer("Администратор успешно удален", show_alert=True)
    await dialog_manager.switch_to(AdminManagementSG.ADMIN_LIST)


@inject_on_click
async def on_new_admin_user_id(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
    admin_service: FromDishka[AdminService],
) -> None:
    if message.text.isdigit():
        permissions = {
            "mailing": True,
            "promos": True,
            "products": True,
            "users": True,
            "admins": True,
            "statistics": True,
        }
        await admin_service.add(
            user_id=int(message.text),
            role=AdminRole.ADMIN,
            permissions=permissions,
        )
        await message.answer("Администратор успешно добавлен")
        await dialog_manager.switch_to(AdminManagementSG.ADMIN_LIST)
    else:
        await message.answer("Введите корректный ID пользователя")


@inject_on_click
async def switch_mailing_permission(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    admin_service: FromDishka[AdminService],
) -> None:
    admin_permissions = dialog_manager.dialog_data["permissions"]
    admin_permissions["mailing"] = True if admin_permissions["mailing"] is False else False
    await admin_service.update(user_id=int(dialog_manager.dialog_data["admin_user_id"]), permissions=admin_permissions)

    await callback_query.answer("Разрешение на рассылку изменено", show_alert=True)


@inject_on_click
async def switch_statistics_permission(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    admin_service: FromDishka[AdminService],
) -> None:
    admin_permissions = dialog_manager.dialog_data["permissions"]
    admin_permissions["statistics"] = True if admin_permissions["statistics"] is False else False
    await admin_service.update(user_id=int(dialog_manager.dialog_data["admin_user_id"]), permissions=admin_permissions)


@inject_on_click
async def switch_admins_permission(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    admin_service: FromDishka[AdminService],
) -> None:
    admin_permissions = dialog_manager.dialog_data["permissions"]
    admin_permissions["admins"] = True if admin_permissions["admins"] is False else False
    await admin_service.update(user_id=int(dialog_manager.dialog_data["admin_user_id"]), permissions=admin_permissions)


@inject_on_click
async def switch_products_permission(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    admin_service: FromDishka[AdminService],
) -> None:
    admin_permissions = dialog_manager.dialog_data["permissions"]
    admin_permissions["products"] = not admin_permissions["products"]
    await admin_service.update(user_id=int(dialog_manager.dialog_data["admin_user_id"]), permissions=admin_permissions)

    await callback_query.answer("Разрешение на управление товарами изменено", show_alert=True)


@inject_on_click
async def switch_users_permission(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    admin_service: FromDishka[AdminService],
) -> None:
    admin_permissions = dialog_manager.dialog_data["permissions"]
    admin_permissions["users"] = not admin_permissions["users"]
    await admin_service.update(user_id=int(dialog_manager.dialog_data["admin_user_id"]), permissions=admin_permissions)

    await callback_query.answer("Разрешение на управление пользователями изменено", show_alert=True)


@inject_on_click
async def switch_promos_permission(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    admin_service: FromDishka[AdminService],
) -> None:
    admin_permissions = dialog_manager.dialog_data["permissions"]
    admin_permissions["promos"] = not admin_permissions["promos"]
    await admin_service.update(user_id=int(dialog_manager.dialog_data["admin_user_id"]), permissions=admin_permissions)
    await callback_query.answer("Разрешение на управление промокодами изменено", show_alert=True)
