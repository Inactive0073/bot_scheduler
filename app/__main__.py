import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs

from fluentogram import TranslatorHub

from redis.asyncio import Redis

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Локальные импорты
from app.config_data.config import Config, load_config
from app.dialogs.setup import get_dialogs
from app.db.base import Base
from app.handlers.commands import commands_router
from app.middlewares import (
    DbSessionMiddleware,
    TrackAllUsersMiddleware,
    TranslatorRunnerMiddleware,
)
from app.utils import (
    create_translator_hub,
    connect_to_nats,
    setup_bot_commands,
    start_delayed_consumer,
)

# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] #%(levelname)-8s %(filename)s:"
    "%(lineno)d - %(name)s - %(message)s",
)

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main() -> None:
    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Подключение к БД
    db_config = config.db

    engine = create_async_engine(url=db_config.dsn, echo=db_config.is_echo)

    # Проверка соединения с СУБД
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    # Создание таблиц
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Подключение к NATS
    nc, js = await connect_to_nats(servers=config.nats.servers)

    # Инициализация хранилаща на базе Redis
    redis = Redis()
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(
            with_destiny=True,
            with_bot_id=True,
        ),
    )

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML, link_preview_is_disabled=True
        ),
    )
    dp = Dispatcher(storage=storage)

    translator_hub: TranslatorHub = create_translator_hub()
    # Sessionmaker для прокидывания сессии в хендлеры
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    # Ставим команды
    await setup_bot_commands(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(commands_router)
    dp.include_routers(*get_dialogs())

    # Регистрируем миддлварь для i18n и бд
    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.update.outer_middleware(DbSessionMiddleware(session_pool=Sessionmaker))
    dp.message.outer_middleware(TrackAllUsersMiddleware())

    # Запускаем функцию настройки проекта для работы с диалогами
    setup_dialogs(dp)

    # Запускаем polling
    try:
        await asyncio.gather(
            dp.start_polling(
                bot,
                js=js,  # прокидываем для получения контекста стрима внутри хендлеров
                delay_send_subject_channel=config.delayed_consumer.subject_channel,
                delay_send_subject_subscriber=config.delayed_consumer.subject_subscriber,
                _translator_hub=translator_hub,  # i18n
            ),
            start_delayed_consumer(
                nc=nc,
                js=js,
                bot=bot,
                subject=config.delayed_consumer.subject_subscriber,
                stream=config.delayed_consumer.stream,
                durable_name=config.delayed_consumer.durable_name,
            ),
            start_delayed_consumer(
                nc=nc,
                js=js,
                bot=bot,
                subject=config.delayed_consumer.subject_channel,
                stream=config.delayed_consumer.stream,
                durable_name=config.delayed_consumer.durable_name,
            ),
        )

    except Exception as e:
        logger.exception(e)
    finally:
        # Закрываем соединение с NATS
        await nc.close()
        logger.info("Connection to NATS closed")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
