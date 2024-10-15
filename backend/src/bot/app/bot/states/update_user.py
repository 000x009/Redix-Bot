from aiogram.fsm.state import State, StatesGroup


class UpdateUserSG(StatesGroup):
    USER_ID = State()
    TOP_UP_BALANCE = State()
    LOWER_BALANCE = State()
    SET_BALANCE = State()
