from aiogram.fsm.state import State, StatesGroup


class MailingSG(StatesGroup):
    MESSAGE = State()
    SEND = State()
    CHECKOUT = State()
    BUTTON = State()
