from nats.js import JetStreamContext
from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup
import logging


logger = logging.getLogger(__name__)

async def delay_message_sending(
    js: JetStreamContext,
    chat_id: int,
    text: str,
    subject: str,
    delay: int = 0,
    keyboard: InlineKeyboardMarkup = None,
) -> None:
    keyboard = keyboard.model_dump_json(exclude_none=True) if keyboard else ''
    headers = {
        "Tg-Delayed-Chat-ID": str(chat_id),
        "Tg-Delayed-Msg-Text": text,
        "Tg-Delayed-Msg-Keyboard": keyboard,
        "Tg-Delayed-Msg-Timestamp": str(datetime.now().timestamp()),
        "Tg-Delayed-Msg-Delay": str(delay),
    }
    await js.publish(subject=subject, headers=headers)
    logger.info(f"Сообщение с текстом {text[:30]} отправлено в очередь на {subject=}"
                f" Пост должен быть доставлен в {datetime.now() + timedelta(seconds=delay)}")