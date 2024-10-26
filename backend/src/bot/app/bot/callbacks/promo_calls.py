from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Chat
from aiogram.fsm.context import FSMContext

from src.bot.app.bot.states import CreatePromoSG, EditPromoSG, InfoPromoSG, DeletePromoSG
from src.bot.app.bot.keyboards import inline

router = Router()


@router.callback_query(F.data == 'admin_promo')
async def promo_handler(
    query: CallbackQuery,
    bot: Bot, 
    event_chat: Chat,
) -> None:
    await bot.edit_message_text(
        message_id=query.message.message_id,
        chat_id=event_chat.id,
        text='💡 Выберите один из предложенных вариантов:',
        reply_markup=inline.admin_promo_kb_markup
    )


@router.callback_query(F.data == 'create_promo')
async def create_promo_handler(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.answer('Введите название промокода.')
    await state.set_state(CreatePromoSG.NAME)


@router.callback_query(F.data == 'edit_promo')
async def edit_promo_handler(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.answer('Введите название или номер промокода который хотите редактировать')
    await state.set_state(EditPromoSG.NAME)


@router.callback_query(F.data.startswith('change_gift_amount'))
async def change_gift_amount_handler(query: CallbackQuery, state: FSMContext) -> None:
    name = query.data.split('|')[-1]
    await state.update_data(name=name)
    await query.message.answer('Введите новую сумму')
    await state.set_state(EditPromoSG.NEW_GIFT_AMOUNT)


@router.callback_query(F.data.startswith('change_uses'))
async def change_uses_handler(query: CallbackQuery, state: FSMContext) -> None:
    name = query.data.split('|')[-1]
    await state.update_data(name=name)
    await query.message.answer('Введите новое число использований')
    await state.set_state(EditPromoSG.NEW_USES)


@router.callback_query(F.data == 'info_promo')
async def info_promo_handler(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.answer('Введите название промокода или его номер о котором хотите узнать информацию')
    await state.set_state(InfoPromoSG.NAME)


@router.callback_query(F.data == 'delete_promo')
async def del_promo_handler(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.answer('Введите название или номер промокода который хотите удалить')
    await state.set_state(DeletePromoSG.NAME)
