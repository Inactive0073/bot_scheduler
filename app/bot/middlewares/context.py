from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ContextMiddleware(BaseMiddleware):
    def __init__(
        self,
        js,
        _translator_hub,
        delay_send_subject_channel,
        delay_send_subject_subscriber,
        web_app_url,
        redis_source,
    ) -> None:
        super().__init__()
        self.js = js
        self._translator_hub = _translator_hub
        self.delay_send_subject_channel = delay_send_subject_channel
        self.delay_send_subject_subscriber = delay_send_subject_subscriber
        self.web_app_url = web_app_url
        self.redis_source = redis_source

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["js"] = self.js
        data["_translator_hub"] = self._translator_hub
        data["delay_send_subject_channel"] = self.delay_send_subject_channel
        data["delay_send_subject_subscriber"] = self.delay_send_subject_subscriber
        data["web_app_url"] = self.web_app_url
        data["redis_source"] = self.redis_source
        return await handler(event, data)
