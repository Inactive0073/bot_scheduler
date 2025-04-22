from sqlalchemy import BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class UserRole(Base):
    __tablename__ = "user_roles"
    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
    )
    role_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("roles.role_id", ondelete="CASCADE")
    )
