from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from aiogram.types import InlineKeyboardMarkup

from app.bot.utils.enums import MediaType


class PostData(BaseModel):
    text: str
    scheduled_time: Optional[datetime] = None
    keyboard: Optional[InlineKeyboardMarkup] = None
    file_id: Optional[str] = None
    type_media: Optional[MediaType]
    has_spoiler: Optional[bool] = False
    notify_status: Optional[bool] = False
    selected_channels: Optional[list[tuple[str, str]]] = None
    selected_customers: Optional[list[int]] = None

    @property
    def data(self):
        data = self.model_dump(mode="json")
        return data
