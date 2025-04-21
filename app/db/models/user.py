from sqlalchemy import BigInteger, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.models.mixins import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    # created_at добавляется из миксина
    timezone_offset: Mapped[int] = mapped_column(
        SmallInteger, default=3, nullable=True, comment="Сдвиг таймзоны"
    )
    timezone: Mapped[int] = mapped_column(
        String, default="Europe/Moscow", nullable=True
    )
    managed_channels: Mapped[list["TgChannel"]] = relationship(  # type: ignore
        secondary="user_channels", back_populates="admins", lazy="dynamic"
    )

    def __repr__(self) -> str:
        if self.last_name is None:
            name = self.first_name
        else:
            name = f"{self.first_name} {self.last_name}"
        return f"[{self.telegram_id} | {self.username}] {name} | {self.utc}. Список каналов: [{self.managed_channels}]"
