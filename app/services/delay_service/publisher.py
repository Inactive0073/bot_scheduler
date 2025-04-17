from nats.js import JetStreamContext
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup

async def delay_message_sending(
    js: JetStreamContext, chat_id: int, message_id: int, subject: str, delay: int = 0,
    keyboard: InlineKeyboardMarkup = None,
) -> None:
    keyboard = keyboard.model_dump_json(exclude_none=True)
    headers = {
        "Tg-Delayed-Chat-ID": str(chat_id),
        "Tg-Delayed-Msg-Text": str(message_id),
        "Tg-Delayed-Msg-Keyboard": keyboard, 
        "Tg-Delayed-Msg-Timestamp": str(datetime.now().timestamp()),
        "Tg-Delayed-Msg-Delay": str(delay),
    }
    await js.publish(subject=subject, headers=headers)
