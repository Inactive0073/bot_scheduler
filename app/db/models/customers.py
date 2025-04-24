from sqlalchemy import SmallInteger, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.models.mixins import TelegramProfileMixin, TimestampMixin


class Customer(TimestampMixin, TelegramProfileMixin, Base):
    __tablename__ = "customers"
    gender: Mapped[str] = mapped_column(String(1), nullable=True)
    bonus: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    percent_cashback: Mapped[int] = mapped_column(
        SmallInteger, default=3, server_default=text("3")
    )
    visits_per_year: Mapped[int] = mapped_column(
        SmallInteger, default=0, server_default=text("0")
    )
    visits: Mapped[int] = mapped_column(
        SmallInteger, default=0, server_default=text("0")
    )
