import logging
import json
from contextlib import suppress
from datetime import datetime, timedelta, timezone

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext

logger = logging.getLogger(__name__)


class DelayedMessageConsumer:
    def __init__(
        self,
        nc: Client,
        js: JetStreamContext,
        bot: Bot,
        subject: str,
        stream: str,
        durable_name: str,
    ) -> None:
        self.nc = nc
        self.js = js
        self.bot = bot
        self.subject = subject
        self.stream = stream
        self.durable_name = durable_name

    async def start(self) -> None:
        self.stream_sub = await self.js.subscribe(
            subject=self.subject,
            stream=self.stream,
            cb=self.on_message,
            durable=self.durable_name,
            manual_ack=True,
        )

    async def on_message(self, msg: Msg):
        logger.info(
            f"Получено сообщение из очереди. Заголовки: {msg.headers=}, Данные: {msg.data=}"
        )

        try:
            # Декодируем payload как JSON
            payload: dict[str, str] = json.loads(msg.data.decode("utf-8"))

            chat_id = payload.get("chat_id")
            post_message = payload.get("text")
            keyboard_data = payload.get("keyboard")
            delay = payload.get("delay", 0)
            tz_label = payload.get("tz_label")
            tz_offset = payload.get("tz_offset")
            notify_status = payload.get("notify_status")
            has_spoiler = payload.get("has_spoiler")
            recipient_type = payload.get("recipient_type")

            # Время публикации
            sent_time_str = payload.get("timestamp")
            tz_info = timezone(timedelta(hours=tz_offset))
            sent_time = datetime.fromisoformat(sent_time_str).replace(tzinfo=tz_info)

            # Проверяем, нужно ли отложить повторно
            if sent_time + timedelta(seconds=delay) > datetime.now(tz=tz_info):
                new_delay = (
                    sent_time + timedelta(seconds=delay) - datetime.now(tz=tz_info)
                ).total_seconds()
                await msg.nak(delay=new_delay)
                return

            # Восстанавливаем клавиатуру, если она есть
            reply_markup = None
            if keyboard_data:
                from aiogram.types import InlineKeyboardMarkup

                reply_markup = InlineKeyboardMarkup.model_validate(keyboard_data)

            # Отправляем сообщение
            with suppress(TelegramBadRequest):
                message = await self.bot.send_message(
                    chat_id=chat_id, text=post_message, reply_markup=reply_markup,
                    disable_notification=notify_status, 
                )
                logger.info(f"Сообщение {message.message_id} успешно отправлено.")

            await msg.ack()

        except Exception as e:
            logger.exception(f"Ошибка при обработке сообщения: {e}")
            await msg.term()  # Или retry / nak, в зависимости от логики

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info("Consumer unsubscribed")
