import os
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Chat, FSInputFile, InputMediaPhoto

from src.bot.app.bot.keyboards import inline


router = Router()


@router.callback_query(F.data == "support")
async def support_handler(query: CallbackQuery, bot: Bot, event_chat: Chat) -> None:
    support_text = """
‼️ Если у вас возникли проблемы - вы можете обратиться в <a href='https://t.me/ParadoxManagers'>поддержку</a>, мы обязательно вам поможем, как можно скорей(ответ сообщений происходит в порядке очереди).
🛡 Никто другой НЕ может представляться от имени поддержки сервиса <a href='https://t.me/loudly_club1'>ParadoxShop</a>
"""
    await bot.edit_message_caption(
        chat_id=event_chat.id,
        message_id=query.message.message_id,
        caption=support_text,
        reply_markup=inline.back_to_main_menu_markup
    )


@router.callback_query(F.data == "main_menu")
async def main_menu(query: CallbackQuery, bot: Bot, event_chat: Chat) -> None:
    media = InputMediaPhoto(
        media=FSInputFile(os.path.normpath("src/bot/app/bot/files/paradox.jpg")),
        caption="🛍 <a href='https://t.me/loudly_club1'>Paradox Shop</a> - сервис внутриигровых покупок и услуг!\n\n🔰 Наш приоритет дать возможность купить любую игровую валюту по лучшим ценам, а также предоставить вам скорейшее получение доната с гарантией безопасности вашего аккаунта",
    )
    await bot.edit_message_media(
        media=media,
        chat_id=event_chat.id,
        message_id=query.message.message_id,
        reply_markup=inline.main_keyboard_markup,
    )
