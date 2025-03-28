"""
Модуль для работы с базой данных Telegram-бота.

Содержит CRUD-операции для моделей User и TgChannel с использованием SQLAlchemy AsyncSession.
Поддерживает PostgreSQL-специфичные UPSERT-операции через on_conflict_do_update.
"""

from typing import cast, Tuple, Union
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.tgchannel import TgChannel
from app.db.models.user import User


async def upsert_user(
    session: AsyncSession,
    telegram_id: int,
    username: str,
    first_name: str,
    last_name: str,
) -> None:
    """Создает или обновляет запись пользователя в базе данных.

    Args:
        session: Асинхронная сессия SQLAlchemy
        telegram_id: Уникальный идентификатор пользователя в Telegram
        username: Юзернейм пользователя (без @)
        first_name: Имя пользователя
        last_name: Фамилия пользователя

    Example:
        await upsert_user(session, 12345, 'john_doe', 'John', 'Doe')
    """
    stmt = upsert(User).values(
        {
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["telegram_id"],
        set_=dict(username=username, first_name=first_name, last_name=last_name),
    )
    await session.execute(stmt)
    await session.commit()


async def get_users(
    session: AsyncSession,
    number_of_users: int,
) -> list[User]:
    """Возвращает список пользователей с сортировкой по имени.

    Args:
        session: Асинхронная сессия SQLAlchemy
        number_of_users: Максимальное количество возвращаемых пользователей

    Returns:
        Список объектов User, отсортированных по first_name

    Example:
        users = await get_users(session, 10)
    """
    stmt = select(User).order_by(User.first_name).limit(number_of_users)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return cast(list[User], users)


async def upsert_channel(
    session: AsyncSession,
    channel_id: int,
    channel_name: str,
    channel_username: str,
    channel_link: str,
    admin_id: int,
) -> None:
    """Создает или обновляет запись Telegram-канала.

    Args:
        session: Асинхронная сессия SQLAlchemy
        channel_id: Уникальный ID канала
        channel_name: Название канала
        channel_username: Юзернейм канала (без @)
        channel_link: Пригласительная ссылка
        admin_id: ID администратора канала

    Example:
        await upsert_channel(session, -100123, 'My Channel', 'mychannel', 'https://t.me/mychannel', 12345)
    """
    stmt = upsert(TgChannel).values(
        {
            "channel_id": channel_id,
            "channel_name": channel_name,
            "channel_username": channel_username,
            "channel_link": channel_link,
            "admin_id": admin_id,
        }
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["channel_id"],
        set_=dict(
            channel_name=channel_name,
            channel_link=channel_link,
            admin_id=admin_id,
        ),
    )
    await session.execute(stmt)
    await session.commit()


async def get_channels(
    session: AsyncSession, telegram_id: int
) -> list[Tuple[Union[str, int]]]:
    """Возвращает каналы, принадлежащие указанному администратору.

    Args:
        session: Асинхронная сессия SQLAlchemy
        telegram_id: ID пользователя-администратора

    Returns:
        Список кортежей с данными каналов в формате:
        (channel_id, name, username, link, admin_id)

    Example:
        channels = await get_channels(session, 12345)
    """
    stmt = select(TgChannel).where(TgChannel.admin_id == telegram_id)
    result = await session.execute(stmt)
    channels = result.scalars()
    return [
        (
            channel.channel_id,
            channel.channel_name,
            channel.channel_username,
            channel.channel_link,
            channel.admin_id,
        )
        for channel in channels
        if channel
    ]


async def get_channel(session: AsyncSession, channel_id: int) -> TgChannel:
    """Возвращает канал по его ID.

    Args:
        session: Асинхронная сессия SQLAlchemy
        channel_id: ID целевого канала

    Returns:
        Объект TgChannel или None, если канал не найден

    Example:
        channel = await get_channel(session, -100123)
    """
    print(f"{channel_id=}")
    stmt = select(TgChannel).where(TgChannel.channel_id == channel_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def delete_channel(session: AsyncSession, channel_id: int) -> bool:
    """Удаляет канал из базы данных.

    Args:
        session: Асинхронная сессия SQLAlchemy
        channel_id: ID канала для удаления

    Returns:
        True если канал был удален, False если канал не найден

    Example:
        success = await delete_channel(session, -100123)
    """
    stmt = delete(TgChannel).where(TgChannel.channel_id == channel_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


async def upsert_caption_channel(
    session: AsyncSession, channel_id: int, caption: str
) -> None:
    """Обновляет подпись для существующего канала.

    Args:
        session: Асинхронная сессия SQLAlchemy
        channel_id: ID целевого канала
        caption: Новая подпись для канала

    Example:
        await upsert_caption_channel(session, -100123, "New channel description")
    """
    stmt = update(TgChannel).where(TgChannel.channel_id == channel_id).values(channel_caption=caption)
    result = await session.execute(stmt)
    await session.commit()


async def get_caption_channel(session: AsyncSession, channel_id: int) -> str:
    """Возвращает подпись канала к посту"""
    stmt = select(TgChannel.channel_caption).where(TgChannel.channel_id == channel_id)
    result = await session.execute(stmt)
    caption = result.first()[0]
    return caption


async def delete_caption_channel(session: AsyncSession, channel_id: int) -> bool:
    """Удаляет подпись к посту"""
    stmt = update(TgChannel).where(TgChannel.channel_id==channel_id).values(channel_caption=None)
    result = await session.execute(stmt)
    await session.commit()
    if result: 
        return True
    
async def toggle_auto_caption_channel(session: AsyncSession, channel_id: int, option: bool) -> bool:
    """Переключает автоподпись канала"""
    stmt = update(TgChannel).where(TgChannel.channel_id==channel_id).values(channel_auto_caption=option)
    result = await session.execute(stmt)
    await session.commit()
    if result:
        return True