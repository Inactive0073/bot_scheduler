import asyncio
import datetime
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fluentogram import TranslatorHub

from .taskiq_broker.broker import broker
from .taskiq_broker.scheduler import scheduler
from .config_data.config import Config, load_config

from .bot.utils import (
    create_translator_hub,
    connect_to_nats,
    setup_bot_commands,
    start_delayed_consumer,
)
from .taskiq_broker.broker import redis_source
from .config_data.config import Config, load_config
from .setup import SetupDependeciesConfig


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] #%(levelname)-8s %(filename)s:"
    "%(lineno)d - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


config: Config = load_config()
dependecies_config: SetupDependeciesConfig = SetupDependeciesConfig(config)

bot: Bot
dp: Dispatcher
bot, dp = dependecies_config.setup_bot()


@asynccontextmanager
async def lifespan(app: FastAPI):
    nc, js = await connect_to_nats(servers=config.nats.servers)  # Connect to NATS
    translator_hub: TranslatorHub = create_translator_hub()
    engine, Sessionmaker = await dependecies_config.setup_database()  # Get session

    await broker.startup()

    dependecies_config.register_middlewares_and_routers(
        dp=dp,
        Sessionmaker=Sessionmaker,
        js=js,
        translator_hub=translator_hub,
        config=config,
        redis_source=redis_source,
    )

    webhook_url = config.get_webhook_url()
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    logger.info(f"Webhook now on {webhook_url}")

    await setup_bot_commands(bot)

    yield

    await nc.close()
    await bot.delete_webhook()
    await broker.shutdown()
    logger.info("Connection to NATS closed")


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
