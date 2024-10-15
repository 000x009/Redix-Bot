from aiogram.fsm.state import State, StatesGroup


class CreatePromoSG(StatesGroup):
    NAME = State()
    GIFT_AMOUNT = State()
    USES = State()


class EditPromoSG(StatesGroup):
    NAME = State()
    NEW_GIFT_AMOUNT = State()
    NEW_USES = State()


class InfoPromoSG(StatesGroup):
    NAME = State()


class DeletePromoSG(StatesGroup):
    NAME = State()
