from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from aiogram.types import InlineKeyboardMarkup

from app.bot.utils.enums import MediaType


class PostData(BaseModel):
    text: str
    schedule_id: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    keyboard: Optional[InlineKeyboardMarkup] = None
    file_id: Optional[str] = None
    has_spoiler: Optional[bool] = False
    disable_notification: Optional[bool] = False
    selected_channels: Optional[list[tuple[str, str]]] = None
    selected_customers: Optional[list[int]] = None
    
    @property
    def time(self):
        return self.scheduled_time.strftime("%H:%M")

    @property
    def data_python(self):
        data = self.model_dump(mode="python")
        return data

    @property
    def data_json(self):
        data = self.model_dump(mode="json")
        return data

    def __getitem__(self, idx):
        pass


