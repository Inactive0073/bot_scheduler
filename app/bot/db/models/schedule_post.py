from sqlalchemy import BigInteger, String, Text, Boolean, Integer, Enum, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.bot.db.models.mixins import TimestampMixin
from app.bot.db import Base


class SchedulePost(TimestampMixin, Base):
    __tablename__ = "schedule_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_type: Mapped[Enum] = mapped_column(Enum, nullable=False)
    scheduled_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    channel_json: Mapped[JSON] = mapped_column(BigInteger, nullable=False)
    post_message: Mapped[Text] = mapped_column(Text, nullable=False)
