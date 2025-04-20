from nats.js import JetStreamContext
from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup
import logging
import json


logger = logging.getLogger(__name__)


async def delay_message_sending(
    js: JetStreamContext,
    chat_id: int,
    text: str,
    subject: str,
    delay: int = 0,
    tz: str = "Europe/Moscow",
    keyboard: InlineKeyboardMarkup = None,
) -> None:
    payload = json.dumps(
        {
            "keyboard": keyboard,
            "text": text,
            "chat_id": chat_id,
            "delay": delay,
            "timestamp": datetime.now().isoformat(),
            "timezone": tz,
        }
    ).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
    }
    await js.publish(subject=subject, headers=headers, payload=payload)
    logger.info(
        f"Сообщение с текстом {text[:30]} отправлено в очередь на {subject=}"
        f" Пост должен быть опубликован в {datetime.now() + timedelta(seconds=delay)}"
    )
