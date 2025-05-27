from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.db.models import Role, UserRole, User


async def get_user_role(session: AsyncSession, telegram_id: int) -> list[str]:
    "Возвращает список ролей пользователя"
    stmt = (
        select(Role.name)
        .join(UserRole, Role.role_id == UserRole.role_id)
        .where(UserRole.user_id == telegram_id)
    )
    async with session.begin():
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_telegram_id_by_username(session: AsyncSession, username: str) -> int | None:
    "Возвращает Telegram ID по никнейму пользователя."
    stmt = select(User.telegram_id).where(User.username == username.lower())
    result = await session.execute(stmt)
    return result.scalar_one_or_none()