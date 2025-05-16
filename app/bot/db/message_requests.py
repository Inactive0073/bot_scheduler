from typing import Literal
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select

from .models.schedule_post import SchedulePost

# ------------------- Schedule Post Operations -------------------
async def upsert_post(
    session: AsyncSession,
    schedule_id: int,
    target_type: Literal["channel", "customer"],
    data_json: dict,
    post_message: str,
    author_id: int
) -> bool:
    """Создает или обновляет запись о запланированном посте в базе данных.

    Args:
        session: Асинхронная сессия SQLAlchemy
        schedule_id: Уникальный идентификатор запланированного поста
        target_type: Тип целевого объекта (канал или пользователь)
        data_json: Данные для отправки в формате JSON
        post_message: Сообщение поста
        author_id: Телеграм ID автора поста

    Example:
        await create_post(session, 1, "channel", {"key": "value"}, "Hello, world!", 12345)
    """
    values = {
        "schedule_id": schedule_id,
        "target_type": target_type,
        "data_json": data_json,
        "post_message": post_message,
        "author_id": author_id
    }
    update_values = {
        "target_type": target_type,
        "data_json": data_json,
        "post_message": post_message,
    }
    stmt = upsert(SchedulePost).values(values).on_conflict_do_update(
        index_elements=["schedule_id"], set_=dict(**update_values)
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


async def get_post(
    session: AsyncSession,
    schedule_id: int,
) -> SchedulePost | None:
    """Получает запись о запланированном посте из базы данных по его ID."""
    result = await session.execute(
        select(SchedulePost).where(SchedulePost.schedule_id == schedule_id)
    )
    return result.scalar_one_or_none()


async def delete_post(
    session: AsyncSession,
    schedule_id: int
) -> bool:
    """Удаляет запись о запланированном посте из базы данных."""
    stmt = delete(SchedulePost).where(SchedulePost.schedule_id == schedule_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0