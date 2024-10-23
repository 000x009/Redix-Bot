from aiogram.fsm.state import State, StatesGroup


class ProductManagementSG(StatesGroup):
    GAMES = State()
    GAME_MANAGEMENT = State()
    CATEGORIES = State()
    CATEGORY_MANAGEMENT = State()
    ADD_CATEGORY_NAME = State()
    ADD_CATEGORY_PHOTO = State()
    ADD_CATEGORY_THREAD_ID = State()
    PRODUCT = State()
    EDIT_PRODUCT_NAME = State()
    EDIT_PRODUCT_DESCRIPTION = State()
    EDIT_PRODUCT_INSTRUCTION = State()
    EDIT_PRODUCT_PRICE = State()
    EDIT_PRODUCT_PHOTO = State()
    ADD_PRODUCT_NAME = State()
    ADD_PRODUCT_DESCRIPTION = State()
    ADD_PRODUCT_INSTRUCTION = State()
    ADD_PRODUCT_PRICE = State()
    ADD_PRODUCT_PHOTO = State()