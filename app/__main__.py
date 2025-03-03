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
from sqlalchemy.ext.asyncio import create_async_engine

# Локальные импорты
from app.config_data.config import Config, load_config
from app.dialogs.setup import get_dialogs
from app.handlers.commands import commands_router
from app.middlewares.i18n import TranslatorRunnerMiddleware
from app.utils.i18n import create_translator_hub
from app.utils.nats_connect import connect_to_nats
from app.utils.start_consumers import start_delayed_consumer

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
    
    engine = create_async_engine(
        url=db_config.dsn,
        echo=db_config.is_echo
    )

    # Открытие нового соединение с базой
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    # Подключение к NATS
    nc, js = await connect_to_nats(servers=config.nats.servers)
    
    # Инициализация хранилаща на базе Redis
    redis = Redis()
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(
            with_destiny=True,
        )    
    )

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML, link_preview_is_disabled=True
        ),
    )
    dp = Dispatcher(storage=storage)

    # Создаем объект типа TranslatorHub
    translator_hub: TranslatorHub = create_translator_hub()

    # Регистриуем роутеры в диспетчере
    dp.include_router(commands_router)
    dp.include_routers(*get_dialogs())

    # Регистрируем миддлварь для i18n
    dp.update.middleware(TranslatorRunnerMiddleware())

    # Запускаем функцию настройки проекта для работы с диалогами
    setup_dialogs(dp)

    # Запускаем polling
    try:
        await dp.start_polling(
                bot, 
                js=js, # прокидываем для получения контекста стрима внутри хендлеров
                delay_del_subject=config.delayed_consumer.subject,
                _translator_hub=translator_hub # i18n
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
