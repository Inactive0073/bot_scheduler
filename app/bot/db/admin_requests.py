from typing import Literal

import logging

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from .models.user_role import UserRole
from .models.user import User
from ..enums.role import UserType

logger = logging.getLogger(__name__)

async def create_employee(
    session: AsyncSession, telegram_id: int, role: UserType) -> bool:
    role_id = {UserType.WAITER: 1, UserType.MANAGER: 2, UserType.ADMIN: 3}.get(role_id)
    if role_id is None:
        logger.error(f"Неверная роль: {role}")
        return False
    stmt = upsert(UserRole).values(
        {
            "user_id": telegram_id,
            "role_id": role_id
        }
    ).on_conflict_do_update(
        index_elements=["user_id"],
        set_=dict(role_id=role_id)
    )
    try:
        result = await session.execute(stmt)
        await session.commit()
        logger.info(f"Сотрудник {telegram_id} успешно создан.")
        return result.rowcount > 0
    except SQLAlchemyError as e:
        logger.error(f"Произошла ошибка при создании нового сотрудника. Ошибка: {e}")
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
) -> tuple:
    """Получает всех сотрудников"""
    stmt = select(User).join(UserRole, UserRole.user_id == User.telegram_id).order_by(User.first_name)
    if size is not None:
        stmt = stmt.limit(size)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users
