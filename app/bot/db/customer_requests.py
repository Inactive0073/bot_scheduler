from datetime import datetime
import logging
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.bot.db.models import Customer, Bonus
from app.bot.utils.generate_qrcode import QRCode


logger = logging.getLogger(__name__)


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
        "qr_code_token": QRCode.generate_token(),
    }
    update_values = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    }
    stmt = upsert(Customer).values(values)
    stmt = stmt.on_conflict_do_update(
        index_elements=["telegram_id"],
        set_=dict(**update_values),
    )
    try:
        async with session.begin():
            await session.execute(stmt)
    except IntegrityError as err:
        raise ValueError(f"Ошибка: {err!r}")


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


async def record_personal_user_data(
    session: AsyncSession,
    telegram_id: int,
    name: str,
    surname: str,
    phone: str,
    email: str,
    birthday: str,
    gender: str,
) -> bool:
    """Добавляет персональные данные пользователя к его профилю в таблице"""
    values = {
        "i_name": name,
        "i_surname": surname,
        "phone": phone,
        "email": email,
        "birthday": birthday,
        "gender": gender,
    }
    stmt = update(Customer).where(Customer.telegram_id == telegram_id).values(values)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


async def get_bonus_info(
    session: AsyncSession, telegram_id: int
) -> tuple[int, datetime, int]:
    """Возвращает баланс бонусов пользователя

    Returns:
        Tuple[summary_bonus, date_expire, bonus_to_expire].
    """
    customer = await session.get(
        Customer, {"telegram_id": telegram_id}, options=[selectinload(Customer.bonuses)]
    )

    bonuses: list[Bonus] = customer.bonuses
    bonuses = sum(bonus.amount for bonus in bonuses)

    nearest_expiring_bonus = min(bonuses, key=lambda bonus: bonus.expire_date)
    expire_date = nearest_expiring_bonus.expire_date
    bonus_to_expire = nearest_expiring_bonus.amount
    return bonuses, expire_date, bonus_to_expire


async def get_card_info(
    session: AsyncSession, telegram_id: int
) -> tuple[int, str | None]:
    """Возвращает информацию по карте клиента"""
    customer = await session.get(Customer, {"telegram_id": telegram_id})
    return customer.qr_code_token, customer.qr_code_file_id


async def update_qr_code_file_id(
    session: AsyncSession, telegram_id: int, file_id
) -> bool:
    """Добавляет file_id запись к клиенту"""
    stmt = (
        update(Customer)
        .where(Customer.telegram_id == telegram_id)
        .values(qr_code_file_id=file_id)
    )

    try:
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0
    except Exception:
        await session.rollback()
        logger.exception("Произошла ошибка при записи file_id")
