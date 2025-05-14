from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.db.models import Role, UserRole


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
