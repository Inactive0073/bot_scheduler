from pydantic import BaseModel
from typing import Optional
from enum import Enum
from aiogram.types import InlineKeyboardMarkup, ContentType


class MediaType(str, Enum):
    photo = "photo"
    video = "video"


class PostData(BaseModel):
    keyboard: Optional[InlineKeyboardMarkup] = None
    file_id: Optional[str] = None
    type_media: Optional[MediaType]
    has_spoiler: Optional[bool] = False
    notify_status: Optional[bool] = False

    @property
    def data(self):
        data = self.model_dump(mode="json")
        return data
