import logging
import asyncio

from dishka.integrations.aiogram import setup_dishka
from dishka import make_async_container

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder


from aiogram_album.ttl_cache_middleware import TTLCacheAlbumMiddleware

from aiogram_dialog import setup_dialogs

from src.bot.app.main.config import settings
from src.main.ioc import DatabaseProvider, DALProvider, ServiceProvider
from src.bot.app.bot.handlers import message_handlers
from src.bot.app.bot.callbacks import callback_handlers
from src.bot.app.bot.dialogs.product import product_management_dialog
from src.bot.app.bot.dialogs.getter import YandexStorageMedia

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    storage = RedisStorage.from_url(
        'redis://redis:6379/0',
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dispatcher = Dispatcher(storage=storage)

    dispatcher.include_routers(
        *message_handlers,
        *callback_handlers,
        product_management_dialog,
    )
    setup_dialogs(dispatcher, message_manager=YandexStorageMedia())

    container = make_async_container(DatabaseProvider(), DALProvider(), ServiceProvider())
    setup_dishka(container=container, router=dispatcher, auto_inject=True)

    TTLCacheAlbumMiddleware(router=dispatcher)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dispatcher.start_polling(bot, skip_updates=True)
    finally:
        await container.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")