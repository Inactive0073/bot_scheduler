from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.mixins import TimestampMixin
from app.db.base import Base


class TgChannel(TimestampMixin, Base):
    __tablename__ = "channels"

    channel_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    channel_name: Mapped[str] = mapped_column(String, nullable=False)
    channel_link: Mapped[str] = mapped_column(String, nullable=False)
    # created_at добавляется из миксина
    admin_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(back_populates="channels")  # type: ignore
