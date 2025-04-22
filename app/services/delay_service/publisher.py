from nats.js import JetStreamContext
from datetime import datetime, timedelta, timezone

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
    tz_label: str = "Europe/Moscow",
    tz_offset: int = 3,
    keyboard: InlineKeyboardMarkup = None,
    file_id: str = None,
    notify_status: bool = True,
    has_spoiler: bool = False,
    recipient_type: str = "bot"
    
) -> None:
    payload = json.dumps(
        {
            "keyboard": keyboard,
            "text": text,
            "chat_id": chat_id,
            "delay": delay,
            "timestamp": datetime.now().isoformat(),
            "tz_label": tz_label,
            "tz_offset": tz_offset,
            "notify_status": notify_status,
            "has_spoiler": has_spoiler,
            "recipient_type": recipient_type,
            
        }
    ).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
    }
    await js.publish(subject=subject, headers=headers, payload=payload)
    logger.info(
        f"Сообщение с текстом {text[:30]} отправлено в очередь на {subject=}"
        f" Пост должен быть опубликован в {datetime.now(tz=timezone(timedelta(hours=tz_offset))) + timedelta(seconds=delay)}"
    )
