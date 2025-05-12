import logging

from aiolimiter import AsyncLimiter

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest

from contextlib import suppress

from taskiq import TaskiqDepends

from ...taskiq_broker.broker import broker

logger = logging.getLogger(__name__)
limiter = AsyncLimiter(max_rate=25, time_period=1)


@broker.task()
async def schedule_message_to_bot(
    chat_id: int,
    text: str,
    delay: int = 0,
    tz_label: str = "Europe/Moscow",
    tz_offset: int = 3,
    keyboard: InlineKeyboardMarkup = None,
    file_id: str = None,
    notify_status: bool = True,
    has_spoiler: bool = False,
    bot: Bot = TaskiqDepends(),
    **kwargs,
) -> None:
    # Отправляем сообщение
    with suppress(TelegramBadRequest):
        message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            disable_notification=notify_status,
        )
        logger.info(f"Сообщение {message.message_id} успешно отправлено.\n")
