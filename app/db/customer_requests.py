from typing import cast, Literal
from sqlalchemy import func, select, delete, update
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db.models import Customer

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
    values =  {
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
    
    
async def get_all_customers(
    session: AsyncSession
) -> list[int]:
    """Возвращает список Telegram-ID пользователей-клиентов.

    Args:
        session: Асинхронная сессия SQLAlchemy.

    Returns:
        List[int]: Список Telegram-ID пользователей.
    """
    stmt = select(Customer.telegram_id)
    result = await session.execute(stmt)
    return result.scalars().all()