import logging
from app.taskiq_broker.broker import broker
import taskiq_aiogram

from aiogram import Bot
from taskiq import TaskiqDepends, Context
from app.config_data.config import load_config, Config
from typing import Annotated, Generator

config: Config = load_config()
logger = logging.getLogger(__name__)

taskiq_aiogram.init(
    broker,
    "app.main:dp",
    # This is path to the bot instance.
    "app.main:bot",
    # You can specify more bots here.
)


@broker.task(task_name="bot_send_test")
async def simple_task(chat_id: int, msg: str, bot: Bot = TaskiqDepends()) -> None:
    print("ITS WORKING")
    print("ITS WORKING")
    await bot.send_message(chat_id=chat_id, text=msg)
