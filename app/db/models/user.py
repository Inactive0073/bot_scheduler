from sqlalchemy import BigInteger, String
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

    channels: Mapped[list["TgChannel"]] = relationship(back_populates="user")  # type: ignore
