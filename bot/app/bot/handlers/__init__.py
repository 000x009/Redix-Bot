from app.bot.handlers import admin, commands, promo


message_handlers = [
    admin.router,
    commands.router,
    promo.router,
]


__all__ = ['message_handlers']
