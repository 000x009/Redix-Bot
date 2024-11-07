from typing import AsyncGenerator
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from src.main.config import settings
from src.services import (
    UserService, ProductService, TransactionService, OrderService, PromoService,
    SupercellAuthService, FeedbackService, FreeKassaService, GameService, YandexStorageClient, AdminService, CategoryService, SupercellClient
)
from src.data.dal import (
    UserDAL, ProductDAL, TransactionDAL, OrderDAL, PromoDAL, FeedbackDAL, GameDAL, AdminDAL, CategoryDAL
)

class Database:
    @staticmethod
    async def get_engine() -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(url=settings.db_connection_url)
        yield engine
        engine.close()

    @staticmethod
    def get_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine)

    @staticmethod
    async def get_async_session(sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
        async with sessionmaker() as session:
            yield session
            await session.close()

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        'src.api.http.supercell_auth',
        'src.api.http.promo',
        'src.api.http.referral_system',
        'src.api.http.payment_system',
        'src.api.http.product',
        'src.api.http.profile',
        'src.api.http.feedback',
        'src.api.http.game',
        'src.api.http.cloud_storage',
        'src.api.http.admin',
        'src.api.http.category',
    ])
    config = providers.Configuration()

    # Database
    engine = providers.Resource(Database.get_engine)
    async_sessionmaker = providers.Factory(
        Database.get_async_sessionmaker,
        engine=engine
    )
    async_session = providers.Resource(
        Database.get_async_session,
        sessionmaker=async_sessionmaker
    )

    # DALs
    user_dal = providers.Factory(UserDAL, session=async_session)
    product_dal = providers.Factory(ProductDAL, session=async_session)
    transaction_dal = providers.Factory(TransactionDAL, session=async_session)
    order_dal = providers.Factory(OrderDAL, session=async_session)
    promo_dal = providers.Factory(PromoDAL, session=async_session)
    feedback_dal = providers.Factory(FeedbackDAL, session=async_session)
    game_dal = providers.Factory(GameDAL, session=async_session)
    admin_dal = providers.Factory(AdminDAL, session=async_session)
    category_dal = providers.Factory(CategoryDAL, session=async_session)

    # Services
    user_service = providers.Factory(UserService, user_dal=user_dal)
    product_service = providers.Factory(ProductService, product_dal=product_dal)
    transaction_service = providers.Factory(TransactionService, transaction_dal=transaction_dal)
    order_service = providers.Factory(OrderService, order_dal=order_dal)
    promo_service = providers.Factory(PromoService, promo_dal=promo_dal)
    supercell_service = providers.Factory(SupercellAuthService)
    feedback_service = providers.Factory(FeedbackService, feedback_dal=feedback_dal)
    freekassa_service = providers.Factory(FreeKassaService)
    game_service = providers.Factory(GameService, game_dal=game_dal)
    admin_service = providers.Factory(AdminService, admin_dal=admin_dal)
    category_service = providers.Factory(CategoryService, category_dal=category_dal)
    supercell_client = providers.Factory(SupercellClient)
    

    yandex_storage_client = providers.Factory(
        YandexStorageClient,
        token=config.YANDEX_STORAGE_TOKEN,
        secret=config.YANDEX_STORAGE_SECRET,
        bucket_name=config.YANDEX_STORAGE_BUCKET_NAME
    )