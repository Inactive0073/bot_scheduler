from typing import cast

from sqlalchemy import select, delete
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
):
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
    stmt = select(User).order_by(User.first_name).limit(number_of_users)
    result = await session.execute(stmt)
    users = result.scalars().all()
    users = cast(list[User], users)
    return users


async def upsert_channel(
    session: AsyncSession,
    channel_id: int,
    channel_name: str,
    channel_username: str,
    channel_link: str,
    admin_id: int,
):
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
) -> list[tuple[str | int]]:
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
    stmt = select(TgChannel).where(TgChannel.channel_id == channel_id)
    result = await session.execute(stmt)
    channel = result.scalars().first()
    return channel


async def delete_channel(session: AsyncSession, channel_id: int):
    stmt = delete(TgChannel).where(TgChannel.channel_id == channel_id)
    result = await session.execute(stmt)
    await session.commit()

    return result.rowcount > 0


async def upsert_caption_channel(session: AsyncSession, channel_id: int, caption: str):
    stmt = upsert(TgChannel).values(
        {"channel_id": channel_id, "channel_caption": caption}
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["channel_id"], set_=dict(channel_caption=caption)
    )
    await session.execute(stmt)
    await session.commit()
