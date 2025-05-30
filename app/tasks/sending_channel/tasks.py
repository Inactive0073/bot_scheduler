import asyncio

from taskiq import TaskiqDepends

import logging
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter

from aiolimiter import AsyncLimiter
from contextlib import suppress

from ...taskiq_broker.broker import broker

logger = logging.getLogger(__name__)


@broker.task(task_name="push_msg_to_channel")
async def send_message_to_channel(
    text: str,
    channels: list[tuple[str, str]],
    keyboard: InlineKeyboardMarkup = None,
    file_id: str = None,
    disable_notification: bool = True,
    has_spoiler: bool = False,
    bot: Bot = TaskiqDepends(),
    limit_message: int = 15,
    **kwargs,
) -> None:
    limiter = AsyncLimiter(limit_message, 1)
    # Отправляем сообщение
    for channel in channels:
        channel_name = "@" + channel[0]  # channel — это кортеж
        async with limiter:
            with suppress(TelegramBadRequest):
                try:
                    message = await bot.send_message(
                        chat_id=channel_name,
                        text=text,
                        reply_markup=keyboard,
                        disable_notification=disable_notification,
                    )
                    logger.info(f"Сообщение {message.message_id} успешно отправлено.\n")
                except TelegramRetryAfter as e:
                    logger.error(
                        f"Превысили допустимое количество отправки сообщений в секунду. Ошибка: {e}"
                    )
                    await asyncio.sleep(5)
