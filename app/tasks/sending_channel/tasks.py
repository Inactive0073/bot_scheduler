from taskiq import TaskiqDepends

import logging
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest

from aiolimiter import AsyncLimiter
from contextlib import suppress

from ...taskiq_broker.broker import broker

logger = logging.getLogger(__name__)


@broker.task(task_name="push_msg_to_bot_now")
async def send_message_to_channel(
    chat_id: int,
    text: str,
    keyboard: InlineKeyboardMarkup = None,
    file_id: str = None,
    notify_status: bool = True,
    has_spoiler: bool = False,
    bot: Bot = TaskiqDepends(),
    limit_message: int = 15,
    **kwargs,
) -> None:
    limiter = AsyncLimiter(limit_message, 1)
    # Отправляем сообщение
    async with limiter:
        with suppress(TelegramBadRequest):
            message = await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=keyboard,
                disable_notification=notify_status,
            )
            logger.info(f"Сообщение {message.message_id} успешно отправлено.\n")
