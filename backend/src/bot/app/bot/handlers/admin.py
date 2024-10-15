import uuid

from aiogram import Router, Bot, F
from aiogram.types import Message, Chat
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from aiogram_album.album_message import AlbumMessage

from dishka import FromDishka

from src.bot.app.bot.filters import AdminFilter
from src.bot.app.bot.keyboards import inline
from src.bot.app.bot.states import MailingSG, UpdateUserSG
from src.services import UserService, TransactionService
from src.schema.transaction import TransactionCause, TransactionType


router = Router()
router.message.filter(AdminFilter())


@router.message(Command("admin"))
async def admin_panel_handler(
    message: Message,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await bot.send_message(
        chat_id=event_chat.id,
        text="Админ-меню",
        reply_markup=inline.admin_menu_kb_markup,
    )


# MAILING HANDLERS
@router.message(MailingSG.MESSAGE, F.media_group_id)
async def mailing_message_handler(
    album_message: AlbumMessage,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    album_photo = [message.photo[-1].file_id for message in album_message]
    media_group = MediaGroupBuilder(caption=album_message.caption)

    for photo in album_photo:
        media_group.add_photo(media=photo)

    await state.update_data(media_group=media_group)
    await bot.send_message(
        chat_id=event_chat.id,
        text="Вы уверены, что хотите разослать это сообщение всем?",
        reply_markup=inline.mailing_choice_kb_markup,
    )
    await state.set_state(MailingSG.CHECKOUT)


@router.message(MailingSG.MESSAGE)
async def mailing_message_handler(
    message: Message,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await state.update_data(message_id=message.message_id)
    await bot.send_message(
        chat_id=event_chat.id,
        text="Вы уверены, что хотите разослать это сообщение всем?",
        reply_markup=inline.mailing_choice_kb_markup,
    )
    await state.set_state(MailingSG.CHECKOUT)


#User Management
@router.message(UpdateUserSG.USER_ID, F.text)
async def update_user_handler(
    message: Message,
    bot: Bot,
    event_chat: Chat,
    user_service: FromDishka[UserService],
    state: FSMContext,
) -> None:
    if not message.text.isdigit():
        return await bot.send_message(chat_id=event_chat.id, text='Введите корректный ID пользователя!')
    
    user = await user_service.get_one_user(user_id=int(message.text))
    if not user:
        await bot.send_message(chat_id=event_chat.id, text='Пользователь с данным ID не был найден!')
        return await state.clear()
    
    await bot.send_message(
        chat_id=event_chat.id,
        text=f'ID: {user.user_id}\nБАЛАНС: {user.balance}',
        reply_markup=inline.update_user_kb_markup(user_id=user.user_id),
    )
    await state.clear()


@router.message(UpdateUserSG.TOP_UP_BALANCE, F.text)
async def top_up_user_handler(
    message: Message,
    bot: Bot,
    event_chat: Chat,
    user_service: FromDishka[UserService],
    transaction_service: FromDishka[TransactionService],
    state: FSMContext,
) -> None:
    if not message.text.isdigit():
        return await bot.send_message(chat_id=event_chat.id, text='Сумма пополнение должна состоять только из цифр!')
    
    state_data = await state.get_data()
    user_id = int(state_data.get('user_id'))

    try:
        top_up_amount = int(message.text)
        user = await user_service.get_one_user(user_id=user_id)
    
        await user_service.update_user(user_id=user_id, balance=user.balance + top_up_amount)
        await transaction_service.add_transaction(
                id=uuid.uuid4(),
                user_id=user_id,
                type=TransactionType.DEPOSIT,
                cause=TransactionCause.ADMIN_DEPOSIT,
                amount=top_up_amount,
                is_successful=True,
            )
        await bot.send_message(chat_id=event_chat.id, text='Вы успешно пополнили пользователю баланс!')
    except Exception as ex:
        print(ex)
        await bot.send_message(chat_id=event_chat.id, text='Упс... Что-то пошло не так.')
    finally:
        await state.clear()


@router.message(UpdateUserSG.LOWER_BALANCE, F.text)
async def lower_user_handler(
    message: Message,
    bot: Bot,
    event_chat: Chat,
    user_service: FromDishka[UserService],
    transaction_service: FromDishka[TransactionService],
    state: FSMContext,
) -> None:
    if not message.text.isdigit():
        return await bot.send_message(chat_id=event_chat.id, text='Сумма, которую вы хотите отнять должна состоять только из цифр!')
    
    state_data = await state.get_data()
    user_id = int(state_data.get('user_id'))
    user = await user_service.get_one_user(user_id=user_id)
    total = user.balance - int(message.text)

    if total < 0:
        await bot.send_message(
            chat_id=event_chat.id,
            text='Сумма на балансе у пользователя не должна быть отрицательной! Попробуйте ввести другое число.',
        )
    else:
        try:
            await user_service.update_user(user_id=user_id, balance=total)
            await transaction_service.add_transaction(
                id=uuid.uuid4(),
                user_id=user_id,
                type=TransactionType.DEBIT,
                cause=TransactionCause.ADMIN_DEBIT,
                amount=int(message.text),
                is_successful=True,
            )
            await bot.send_message(chat_id=event_chat.id, text='Вы успешно отняли пользователю баланс!')
        except Exception as ex:
            print(ex)
            await bot.send_message(chat_id=event_chat.id, text='Упс... Что-то пошло не так.')
        finally:
            await state.clear()


@router.message(UpdateUserSG.SET_BALANCE, F.text)
async def set_user_balance_handler(
    message: Message,
    bot: Bot,
    event_chat: Chat,
    user_service: FromDishka[UserService],
    state: FSMContext,
) -> None:
    if not message.text.isdigit():
        return await bot.send_message(chat_id=event_chat.id, text='Сумма, которую вы хотите установить должна состоять только из цифр!')
    
    state_data = await state.get_data()
    user_id = state_data.get('user_id')

    try:
        await user_service.update_user(user_id=int(user_id), balance=int(message.text))
        await bot.send_message(chat_id=event_chat.id, text='Вы успешно установили пользователю баланс!')
    except Exception as ex:
        print(ex)
        await bot.send_message(chat_id=event_chat.id, text='Упс... Что-то пошло не так.')
    finally:
        await state.clear()
