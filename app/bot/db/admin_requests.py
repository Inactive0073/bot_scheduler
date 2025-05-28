from typing import Literal

import logging

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from .models.user_role import UserRole
from .models.user import User
from ..utils.enums.role import UserType
from ..utils.exc import NotFoundError, AlreadyHaveAllRoles

from .common_requests import user_exists

logger = logging.getLogger(__name__)

async def create_employee(
    session: AsyncSession, telegram_id: int, role: UserType
) -> bool:
    role_id = {UserType.WAITER: 1, UserType.MANAGER: 2, UserType.ADMIN: 3}.get(role)
    if role_id is None:
        logger.error(f"Неверная роль: {role}")
        return False
    is_exists = await user_exists(session=session, telegram_id=telegram_id)
    if not is_exists:
        logger.error(f"Администратор пытается добавить пользователя {telegram_id}, который не запустил бота или такого пользователя вообще не существует.")
        raise NotFoundError
    # Проверка, есть ли у пользователя все роли
    all_roles = {1, 2, 3}
    stmt_check = select(UserRole.role_id).where(UserRole.user_id == telegram_id)
    result = await session.execute(stmt_check)
    current_roles = {row.role_id for row in result}
    if current_roles == all_roles:
        logger.info(f"Пользователь {telegram_id} уже имеет все роли.")
        raise AlreadyHaveAllRoles
    # Добавление роли, если она еще не назначена
    stmt = insert(UserRole).values(
        user_id=telegram_id,
        role_id=role_id
    ).on_conflict_do_nothing(
        index_elements=['user_id', 'role_id']
    )
    try:
        result = await session.execute(stmt)
        await session.commit()
        if result.rowcount > 0:
            logger.info(f"Роль {role} добавлена для сотрудника {telegram_id}.")
            return True
        else:
            logger.info(f"Роль {role} уже назначена сотруднику {telegram_id}.")
            return False
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Произошла ошибка при добавлении роли для сотрудника {telegram_id}. Ошибка: {e}")
        return False


async def kick_employee(
    session: AsyncSession, telegram_id: int
) -> bool:
    stmt = delete(UserRole).where(UserRole.user_id == telegram_id)
    try:
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        logger.error(f"Произошла ошибка при удалении сотрудника. Ошибка: {e}")
        return False
    

async def get_employee(
    session: AsyncSession, telegram_id: int
) -> User:
    stmt = select(User).join(UserRole, UserRole.user_id == telegram_id).where(User.telegram_id == telegram_id)
    try:
        result = await session.execute(stmt)
        return result.one_or_none()
    except SQLAlchemyError as e:
        logger.error(f"Произошла ошибка при получении сотрудника {telegram_id}. Ошибка: {e}")


async def get_employees(
    session: AsyncSession, size: int | None = None
) -> list[User]:
    """Получает всех сотрудников с их ролями."""
    stmt = (
        select(User)
        .join(UserRole, UserRole.user_id == User.telegram_id)
        .distinct()
        .order_by(User.first_name)
    )
    if size is not None:
        stmt = stmt.limit(size)
    result = await session.execute(stmt)
    return result.scalars().all()
