import logging
import json
from contextlib import suppress
from datetime import datetime, timedelta, timezone
from environs import Env

from aiolimiter import AsyncLimiter
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext

logger = logging.getLogger(__name__)
env = Env()


class DelayedMessageConsumer:
    limiter = AsyncLimiter(max_rate=25, time_period=1)

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
        if self.subject == env("NATS_DELAYED_CONSUMER_SUBJECT_CHANNEL"):
            logger.info(
                "Создание подписки на поток для каналов",
                extra={
                    "subject": self.subject,
                    "stream": self.stream,
                    "durable": f"{self.durable_name}_channel",
                },
            )
            self.stream_sub = await self.js.subscribe(
                subject=self.subject,
                stream=self.stream,
                cb=self.on_message_channel,
                durable=self.durable_name + "_channel",
                manual_ack=True,
            )
        elif self.subject == env("NATS_DELAYED_CONSUMER_SUBJECT_SUBSCRIBER"):
            logger.info(
                "Создание подписки на поток для подписчиков",
                extra={
                    "subject": self.subject,
                    "stream": self.stream,
                    "durable": f"{self.durable_name}_bot",
                },
            )
            self.stream_sub = await self.js.subscribe(
                subject=self.subject,
                stream=self.stream,
                cb=self.on_message_bot,
                durable=self.durable_name + "_bot",
                manual_ack=True,
            )

    async def on_message_channel(self, msg: Msg):
        logger.info(
            "Получено новое сообщение для канала",
            extra={
                "subject": msg.subject,
                "headers": dict(msg.headers),
            },
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
            disable_notification = payload.get("disable_notification")
            has_spoiler = payload.get("has_spoiler")

            # Время публикации
            sent_time_str = payload.get("timestamp")
            tz_info = timezone(timedelta(hours=tz_offset))
            sent_time = datetime.fromisoformat(sent_time_str).replace(tzinfo=tz_info)

            # Проверяем, нужно ли отложить повторно
            if sent_time + timedelta(seconds=delay) > datetime.now(tz=tz_info):
                new_delay = (
                    sent_time + timedelta(seconds=delay) - datetime.now(tz=tz_info)
                ).total_seconds()
                logger.info(
                    "Сообщение отложено",
                    extra={
                        "chat_id": chat_id,
                        "new_delay": new_delay,
                        "sent_time": sent_time.isoformat(),
                    },
                )
                await msg.nak(delay=new_delay)
                return

            # Отправляем сообщение
            with suppress(TelegramBadRequest):
                message = await self.bot.send_message(
                    chat_id=chat_id,
                    text=post_message,
                    reply_markup=keyboard_data,
                    disable_notification=disable_notification,
                )
                logger.info(
                    "Сообщение успешно отправлено в канал",
                    extra={
                        "message_id": message.message_id,
                        "chat_id": chat_id,
                    },
                )

            await msg.ack()
        except Exception as e:
            logger.exception(
                "Ошибка при обработке сообщения для канала",
                extra={
                    "error": str(e),
                    "subject": msg.subject,
                },
            )
            await msg.term()  # Или retry / nak, в зависимости от логики

    async def on_message_bot(self, msg: Msg):
        logger.info(
            "Получено новое сообщение для рассылки в боте",
            extra={
                "subject": msg.subject,
                "headers": dict(msg.headers),
            },
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
            disable_notification = payload.get("disable_notification")
            has_spoiler = payload.get("has_spoiler")

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

            # Отправляем сообщение
            async with self.limiter:
                with suppress(TelegramBadRequest):
                    message = await self.bot.send_message(
                        chat_id=chat_id,
                        text=post_message,
                        reply_markup=keyboard_data,
                        disable_notification=disable_notification,
                    )
                    logger.info(f"Сообщение {message.message_id} успешно отправлено.\n")
                    await msg.ack()

        except Exception as e:
            logger.exception(f"Ошибка при обработке сообщения: {e}")
            await msg.term()  # Или retry / nak, в зависимости от логики

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info(
                "Отписка от потока сообщений",
                extra={
                    "subject": self.subject,
                    "stream": self.stream,
                },
            )
