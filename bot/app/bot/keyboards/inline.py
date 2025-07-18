from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from app.main.config import dev_config


main_keyboard_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Открыть Магазин", web_app=WebAppInfo(url="https://redixshop.com/"))
        ],
        [
            InlineKeyboardButton(text="Поддержка", callback_data="support"),
            InlineKeyboardButton(text="Правила", url="https://teletype.in/@redixempire/RedixShopBotFaq"),
        ],
    ]
)

def cancel_without_reason_kb_markup(order_id: UUID) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Без причины", callback_data=f"cancel_order:{order_id}")
            ]
        ]
    )


def web_app_button(game_id: int) -> InlineKeyboardMarkup:
    if int(game_id) > 0:
        url = f"https://redixshop.com/game?id={game_id}"
    elif int(game_id) == -1:
        url = "https://redixshop.com/"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="КУПИТЬ", web_app=WebAppInfo(url=url))
            ]
        ]
    )



def accepted_friend_request_kb_markup(order_id: UUID) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm_request:{order_id}")
            ]
        ]
    )

def accept_friend_request_kb_markup(order_id: UUID) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Принял заявку", callback_data=f"accept_request:{order_id}")
            ]
        ]
    )

back_to_main_menu_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"),
        ],
    ]
)


def admin_menu_kb_markup(admin_permissions: dict[str, bool]) -> InlineKeyboardMarkup:
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="Рассылка", callback_data="admin_mailing")])
    keyboard.append([InlineKeyboardButton(text="Промокоды", callback_data="admin_promo")])
    keyboard.append([InlineKeyboardButton(text="Управление товарами", callback_data="product_management")])
    keyboard.append([InlineKeyboardButton(text="Управление пользователями", callback_data="user_management")])
    keyboard.append([InlineKeyboardButton(text="Управление администраторами", callback_data="admin_management")])
    keyboard.append([InlineKeyboardButton(text="Статистика бота", callback_data="bot_statistics")])
    keyboard.append([InlineKeyboardButton(text="Звезды", callback_data="stars_management")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def change_stars_config_kb_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Изменить курс", callback_data="change_stars_rate")
            ],
            [
                InlineKeyboardButton(text="Изменить API Hash", callback_data="change_stars_api_hash")
            ],
            [
                InlineKeyboardButton(text="Изменить API Cookie", callback_data="change_stars_api_cookie")
            ],
            [
                InlineKeyboardButton(text="Изменить мнемонику", callback_data="change_stars_mnemonic")
            ]
        ]
    )

back_to_apanel_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Вернуться назад", callback_data="back_apanel"),
        ],
    ]
)


mailing_choice_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="confirm_mailing"),
            InlineKeyboardButton(text="Нет", callback_data="cancel_mailing"),
        ],
    ]
)


admin_promo_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='➕ Создать промокод', callback_data='create_promo'),
            InlineKeyboardButton(text='🔧 Редактировать промокод', callback_data='edit_promo')
        ],
        [
            InlineKeyboardButton(text='ℹ️ Информация о промокоде', callback_data='info_promo'),
            InlineKeyboardButton(text='❌ Удалить промокод', callback_data='delete_promo')
        ],
        [
            InlineKeyboardButton(text="↪️ Вернуться назад", callback_data="back_apanel"),
        ],
    ]
)


def edit_promo_kb_markup(name: int | str) -> InlineKeyboardMarkup:
    kb_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='💵 Изменить сумму', callback_data=f'change_gift_amount|{name}'),
                InlineKeyboardButton(text='🔧 Изменить кол-во использований', callback_data=f'change_uses|{name}')
            ]
        ]
    )
    return kb_markup


def update_user_kb_markup(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Пополнить баланс', callback_data=f'top_up_balance:{user_id}'),
            ],
            [
                InlineKeyboardButton(text='Отнять баланс', callback_data=f'lower_balance:{user_id}'),
            ],
            [
                InlineKeyboardButton(text='Установить баланс', callback_data=f'set_balance:{user_id}'),
            ],
        ]
    )


def order_confirmation_kb_markup(order_id: UUID) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'confirm_order:{order_id}'),
            ],
            [
                InlineKeyboardButton(text='❌ Отменить', callback_data=f'cancel_order_reason:{order_id}'),
            ],
        ]
    )


def gift_order_confirmation_kb_markup(order_id: UUID) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Добавлено в друзья', callback_data=f'add_to_friends:{order_id}'),
            ],
            [
                InlineKeyboardButton(text='❌ Отменить', callback_data=f'cancel_order_reason:{order_id}'),
            ],
        ]
    )


def take_order_kb_markup(order_id: UUID) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Взяться за заказ', callback_data=f'take_order:{order_id}')
            ]
        ]
    )


def post_feedback_kb_markup(order_id: UUID) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
        [
                InlineKeyboardButton(text='👀 Оставить отзыв', web_app=WebAppInfo(url=f'https://redixshop.com/post-feedback/{order_id}'))
            ]
        ]
    )
