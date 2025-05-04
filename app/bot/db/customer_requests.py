from dataclasses import dataclass
from datetime import datetime
from typing import cast, Literal
from sqlalchemy import func, select, delete, update
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.bot.db.models import Customer, Bonus


async def upsert_customer(
    session: AsyncSession,
    telegram_id: int,
    first_name: str,
    last_name: str = None,
    username: str = None,
) -> None:
    """Создает или обновляет запись клиента в базе данных.

    Args:
        session: Асинхронная сессия SQLAlchemy
        telegram_id: Уникальный идентификатор пользователя в Telegram
        first_name: Имя пользователя
        last_name: Фамилия пользователя
        username: Юзернейм пользователя (без @)

    Example:
        await upsert_customer(session, 12345, 'john_doe', 'John', 'Doe')
    """
    values = {
        "telegram_id": telegram_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    }
    stmt = upsert(Customer).values(values)
    stmt = stmt.on_conflict_do_update(
        index_elements=["telegram_id"],
        set_=dict(**values, updated_at=func.now()),
    )
    try:
        await session.execute(stmt)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ValueError("Ошибка: {e!r}")


async def get_all_customers(session: AsyncSession) -> list[int]:
    """Возвращает список Telegram-ID пользователей-клиентов.

    Args:
        session: Асинхронная сессия SQLAlchemy.

    Returns:
        List[int]: Список Telegram-ID пользователей.
    """
    stmt = select(Customer.telegram_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def record_personal_user_data(session: AsyncSession, telegram_id: int, name: str, surname: str, phone: str, email: str, birthday: str, gender: str) -> bool:
    """Добавляет персональные данные пользователя к его профилю в таблице"""
    values = {
        "i_name": name,
        "i_surname": surname,
        "phone": phone,
        "email": email,
        "birthday": birthday,
        "gender": gender
    }
    stmt = update(Customer).where(Customer.telegram_id == telegram_id).values(values)
    result = await session.execute(stmt)
    return result.rowcount() > 0


async def get_bonus_info(session: AsyncSession, telegram_id: int):
    """Возвращает баланс бонусов пользователя"""
    customer = await session.get(
        Customer, {"telegram_id": telegram_id},
        options=[selectinload(Customer.bonuses)]
    )

    bonuses: list[Bonus] = customer.bonuses
    bonuses = sum(bonus.amount for bonus in bonuses)
    
    nearest_expiring_bonus = min(bonuses, key=lambda bonus: bonus.expire_date)
    expire_date = nearest_expiring_bonus.expire_date
    bonus_to_expire = nearest_expiring_bonus.amount
    

