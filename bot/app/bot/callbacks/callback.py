import os
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Chat, FSInputFile, InputMediaPhoto

from app.bot.keyboards import inline


router = Router()


@router.callback_query(F.data == "support")
async def support_handler(query: CallbackQuery, bot: Bot, event_chat: Chat) -> None:
    support_text = """
❓ Если у вас возникнут проблемы или вопросы, обратитесь в нашу <a href='https://t.me/RedixSupportBot'>службу поддержки</a>. Мы постараемся помочь вам как можно быстрее (ответ на сообщения дается в порядке очереди).

❗️ Обязательно проверьте, есть ли ответ на ваш вопрос в нашем разделе <a href='https://teletype.in/@redixempire/RedixShopBotFaq'>FAQ</a>. Ведь там вы сможете найти ответы на многие часто задаваемые вопросы.
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
        media=FSInputFile(os.path.normpath("app/bot/files/redix.jpg")),
        caption="🌟 Добро пожаловать!\n\n🐱 <a href='https://t.me/RedixEmpire'>Redix Shop</a> - это сервис для покупки различных внутриигровых товаров. Мы делаем всё возможное, чтобы обеспечить быструю, надёжную и качественную выдачу товаров по лучшим ценам, что подтверждается нашими <a href='https://t.me/redixempire_otz'>отзывами</a>",
    )
    await bot.edit_message_media(
        media=media,
        chat_id=event_chat.id,
        message_id=query.message.message_id,
        reply_markup=inline.main_keyboard_markup,
    )
