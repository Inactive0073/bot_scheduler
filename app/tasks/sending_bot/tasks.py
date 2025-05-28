import logging
import taskiq_aiogram

from aiolimiter import AsyncLimiter

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, ContentType
from aiogram.exceptions import TelegramBadRequest

from contextlib import suppress

from taskiq import TaskiqDepends

from ...taskiq_broker.broker import broker

logger = logging.getLogger(__name__)

taskiq_aiogram.init(
    broker,
    "app.main:dp",
    # This is path to the bot instance.
    "app.main:bot",
    # You can specify more bots here.
)


BOT_LIMIT_MESSAGE = AsyncLimiter(20, 1)


@broker.task(task_name="push_msg_to_bot_now")
async def send_message_bot_subscribers(
    chat_id: int,
    text: str,
    keyboard: InlineKeyboardMarkup = None,
    file_id: str = None,
    type_media: ContentType = ContentType.PHOTO,
    notify_status: bool = True,
    has_spoiler: bool = False,
    bot: Bot = TaskiqDepends(),
    **kwargs,
) -> None:
    # Отправляем сообщение
    if file_id is None:
        async with BOT_LIMIT_MESSAGE:
            with suppress(TelegramBadRequest):
                message = await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=keyboard,
                    disable_notification=notify_status,
                )
                logger.info(f"Сообщение {message.message_id} успешно отправлено.\n")
    elif file_id:
        async with BOT_LIMIT_MESSAGE:
            with suppress(TelegramBadRequest):
                message = await bot.send_photo(
                    chat_id=chat_id,
                    photo=file_id,
                    caption=text,
                    has_spoiler=has_spoiler,
                    reply_markup=keyboard,
                    disable_notification=notify_status,
                )
                logger.info(f"Сообщение {message.message_id} успешно отправлено.\n")


@broker.task(task_name="push_msg_to_bot_later")
async def send_schedule_message_bot_subscribers(
    chat_id: int,
    text: str,
    keyboard: InlineKeyboardMarkup = None,
    file_id: str = None,
    type_media: ContentType = ContentType.PHOTO,
    notify_status: bool = True,
    has_spoiler: bool = False,
    bot: Bot = TaskiqDepends(),
    **kwargs,
) -> None:
    # Отправляем сообщение
    if file_id is None:
        async with BOT_LIMIT_MESSAGE:
            with suppress(TelegramBadRequest):
                message = await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=keyboard,
                    disable_notification=notify_status,
                )
                logger.info(f"Сообщение {message.message_id} успешно отправлено.\n")
    elif file_id:
        async with BOT_LIMIT_MESSAGE:
            with suppress(TelegramBadRequest):
                message = await bot.send_photo(
                    chat_id=chat_id,
                    photo=file_id,
                    caption=text,
                    has_spoiler=has_spoiler,
                    reply_markup=keyboard,
                    disable_notification=notify_status,
                )
                logger.info(f"Сообщение {message.message_id} успешно отправлено.\n")
