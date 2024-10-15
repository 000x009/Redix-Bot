from src.bot.app.bot.callbacks import admin, callback, promo_calls


callback_handlers = [
    admin.router,
    callback.router,
    promo_calls.router,
]


__all__ = ['callback_handlers']
