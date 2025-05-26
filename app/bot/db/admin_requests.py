from typing import Literal

import logging

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from .models.user_role import UserRole
from .models.user import User

logger = logging.getLogger(__name__)

async def create_employee(
    session: AsyncSession, telegram_id: int, role_id: Literal["waiter", "manager", "admin"]) -> bool:
    role_id = {"waiter": 1, "manager": 2, "admin": 3}.get(role_id)
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
        await session.execute(stmt)
        await session.commit()
        logger.info(f"Сотрудник {telegram_id} успешно создан.")
    except SQLAlchemyError as e:
        logger.error(f"Произошла ошибка при создании нового сотрудника. Ошибка: {e}")

async def kick_employee(
    session: AsyncSession, telegram_id: int
) -> bool:
    stmt = delete(UserRole).where(UserRole.user_id == telegram_id)
    try:
        await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        logger.error(f"Произошла ошибка при удалении сотрудника. Ошибка: {e}")


async def get_employee(
    session: AsyncSession, telegram_id: int
):
    stmt = select(User).join(UserRole, UserRole.user_id == telegram_id).where(User.telegram_id == telegram_id)
    try:
        await session.execute(stmt)
    except SQLAlchemyError as e:
        logger.error(f"Произошла ошибка при получении сотрудника {telegram_id}. Ошибка: {e}")


async def get_employees(
    session: AsyncSession, size: int | None = None
) -> tuple:
    """Получает всех сотрудников"""
    if size is None:
        stmt = select(UserRole)


