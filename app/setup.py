import logging
from typing import Literal
from aiogram import Bot, Dispatcher

from aiogram.client.default import DefaultBotProperties

from aiogram_dialog import setup_dialogs
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from dataclasses import dataclass

from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.enums import ParseMode

from taskiq_redis import RedisAsyncResultBackend, RedisScheduleSource
from taskiq import TaskiqScheduler

from app.bot.db.base import Base
from app.bot.middlewares import (
    DbSessionMiddleware,
    TrackAllUsersMiddleware,
    TranslatorRunnerMiddleware,
    ContextMiddleware,
)
from app.bot.dialogs.setup import get_dialogs
from app.bot.handlers.commands import commands_router
from app.config_data.config import Config

from app.taskiq_broker.broker import broker

logger = logging.getLogger(__name__)

@dataclass
class SetupDependeciesConfig:
    config: Config


    async def setup_database(self) -> tuple[AsyncEngine, AsyncSession]:
        engine = create_async_engine(url=self.config.db.dsn, echo=self.config.db.is_echo)
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))  # Проверка соединения
            await conn.run_sync(Base.metadata.create_all)
        Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
        logger.info("Соединение к БД успешно проверено. ")
        return engine, Sessionmaker

    def setup_bot(self) -> tuple[Bot, Dispatcher]:
        redis = Redis()
        storage = RedisStorage(
            redis=redis,
            key_builder=DefaultKeyBuilder(
                with_destiny=True,
                with_bot_id=True,
            ),
        )
        dp = Dispatcher(storage=storage)
        bot = Bot(
            token=self.config.tg_bot.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML, link_preview_is_disabled=True
            ),
        )
        return bot, dp

    @staticmethod
    def register_middlewares_and_routers(
        dp: Dispatcher, 
        Sessionmaker: AsyncSession,
        js, 
        translator_hub,
        config: Config,
        redis_source: RedisScheduleSource,
    ):
        # Регистриуем роутеры в диспетчере
        dp.include_router(commands_router)
        dp.include_routers(*get_dialogs())

        # Регистрируем миддлварь для i18n и бд
        dp.update.middleware(TranslatorRunnerMiddleware())
        dp.update.outer_middleware(DbSessionMiddleware(session_pool=Sessionmaker))
        dp.update.outer_middleware(
            ContextMiddleware(
                js=js,
                _translator_hub=translator_hub,
                delay_send_subject_channel=config.delayed_consumer.subject_channel,
                delay_send_subject_subscriber=config.delayed_consumer.subject_subscriber,
                web_app_url=config.tg_bot.url,
                redis_source=redis_source,
            )
        )
        dp.message.outer_middleware(TrackAllUsersMiddleware())

        # Запускаем функцию настройки проекта для работы с диалогами
        setup_dialogs(dp)

    
