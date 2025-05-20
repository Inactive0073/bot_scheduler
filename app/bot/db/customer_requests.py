from datetime import datetime, timedelta
import logging
from sqlalchemy import select, update, func, case, and_
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

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
        await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Database error: {e}")
        return False
        

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
    """Добавляет персональные данные пользователя к его профилю в таблице и добавляет 100 приветственных бонусов к аккаунту"""
    values = {
        "i_name": name,
        "i_surname": surname,
        "phone": phone,
        "email": email,
        "birthday": birthday,
        "gender": gender,
    }
    user_stmt = (
        update(Customer).where(Customer.telegram_id == telegram_id).values(values)
    )
    bonus_stmt = upsert(Bonus).values(
        {"customer_id": telegram_id, "amount": 100, "source_type": "bonus"}
    )

    try:
        async with session.begin():
            user_result = await session.execute(user_stmt)
            await session.execute(bonus_stmt)
        return user_result.rowcount > 0

    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Database error: {e}")
        return False


async def get_bonus_info(
    session: AsyncSession, telegram_id: int
) -> tuple[int, datetime | None, int]:
    """Возвращает баланс бонусов пользователя

    Returns:
        Tuple[summary_bonus, date_expire, bonus_to_expire]:
            - summary_bonus: общий баланс бонусов
            - date_expire: ближайшая дата истечения баллов или None
            - bonus_to_expire: сумма баллов, истекающих в ближайшую дату
    """
    now = datetime.now()
    min_expire_subquery = (
        select(func.coalesce(func.min(Bonus.expire_date), now + timedelta(weeks=52)))
        .where(and_(Bonus.customer_id == telegram_id, Bonus.expire_date > now))
        .scalar_subquery()
    )
    stmt = select(
        func.sum(Bonus.amount).label("total_points"),
        min_expire_subquery.label("nearest_expiration_date"),
        func.sum(
            case((Bonus.expire_date == min_expire_subquery, Bonus.amount), else_=0)
        ).label("bonus_to_expire"),
    ).where(Bonus.customer_id == telegram_id)

    result = await session.execute(stmt)
    row = result.one_or_none()

    if row:
        total_points, nearest_expiration_date, bonus_to_expire = row
        # Если nearest_expiration_date равна now + 52 недели, значит нет будущих истечений
        if nearest_expiration_date.date() == (now + timedelta(weeks=52)).date():
            nearest_expiration_date = None
        return (
            int(total_points or 0),
            nearest_expiration_date,
            int(bonus_to_expire or 0),
        )
    return None


async def get_card_info(
    session: AsyncSession, telegram_id: int
) -> tuple[int, str | None]:
    """Возвращает информацию по карте клиента"""
    customer = await session.get(Customer, {"telegram_id": telegram_id})
    return customer.qr_code_token, customer.qr_code_file_id


async def has_customer_detail_info(session: AsyncSession, telegram_id: int) -> bool:
    """Возвращает факт наличия данных в форме"""
    customer = await session.get(Customer, {"telegram_id": telegram_id})
    return bool(customer)


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
