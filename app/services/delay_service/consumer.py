import logging
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
        # Получаем из заголовков сообщения время отправки и время задержки
        sent_time = datetime.fromtimestamp(
            float(msg.headers.get("Tg-Delayed-Msg-Timestamp")), tz=timezone.utc
        )
        delay = int(msg.headers.get("Tg-Delayed-Msg-Delay"))

        # Проверяем наступило ли время обработки сообщения
        if sent_time + timedelta(seconds=delay) > datetime.now().astimezone():
            # Если время обработки не наступило - вычисляем сколько секунд осталось до обработки
            new_delay = (
                sent_time + timedelta(seconds=delay) - datetime.now().astimezone()
            ).total_seconds()
            # Отправляем nak с временем задержки
            await msg.nak(delay=new_delay)
        else:
            # Если время обработки наступило - пытаемся отправить сообщение
            chat_id = msg.headers.get("Tg-Delayed-Chat-ID")
            post_message = msg.headers.get("Tg-Delayed-Msg-Text")
            keyboard = msg.headers.get("Tg-Delayed-Msg-Keyboard")
            with suppress(TelegramBadRequest):
                await self.bot.send_message(
                    chat_id=chat_id, text=post_message, reply_markup=keyboard
                )
            await msg.ack()

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info("Consumer unsubscribed")
