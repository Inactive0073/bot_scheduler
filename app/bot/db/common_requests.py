from typing import cast, Literal
from sqlalchemy import func, select, delete, update
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.bot.db.models import User, Role, UserRole


async def get_user_role(session: AsyncSession, telegram_id: int) -> list[str]:
    "Возвращает список ролей пользователя"
    stmt = (
        select(Role.name)
        .join(UserRole, Role.role_id == UserRole.role_id)
        .where(UserRole.user_id == telegram_id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()
