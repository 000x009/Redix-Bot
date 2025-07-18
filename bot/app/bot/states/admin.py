from aiogram.fsm.state import StatesGroup, State


class AdminManagementSG(StatesGroup):
    ADMIN_LIST = State()
    ADMIN_INFO = State()
    REMOVE_ADMIN = State()
    ADD_ADMIN = State()
    SWITCH_MAILING_PERMISSION = State()
    SWITCH_PRODUCT_MANAGEMENT_PERMISSION = State()
    SWITCH_USER_MANAGEMENT_PERMISSION = State()
    SWITCH_PROMO_MANAGEMENT_PERMISSION = State()


class GiftOrderManagementSG(StatesGroup):
    MESSAGE_TO_USER = State()


class ChangeStarsConfigSG(StatesGroup):
    RATE = State()
    API_HASH = State()
    API_COOKIE = State()
    MNEMONIC = State()
