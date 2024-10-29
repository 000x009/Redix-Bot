from aiogram.fsm.state import State, StatesGroup


class CancelOrderSG(StatesGroup):
    REASON = State()
