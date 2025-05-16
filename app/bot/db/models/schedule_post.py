from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from typing import Optional

from app.bot.db.models.mixins import TimestampMixin
from app.bot.db import Base


class SchedulePost(TimestampMixin, Base):
    __tablename__ = "schedule_posts"

    schedule_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True
    )
    target_type: Mapped[str]
    scheduled_time: Mapped[datetime]
    data_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    post_message: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE")
    )
