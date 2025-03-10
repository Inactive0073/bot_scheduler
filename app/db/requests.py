from typing import cast

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

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


async def upsert_channel(
    session: AsyncSession,
    channel_id: int,
    channel_name: str,
    channel_link: str,
    admin_id: int,
):
    stmt = upsert(TgChannel).values(
        {
            "channel_id": channel_id,
            "channel_name": channel_name,
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


async def get_channels(session: AsyncSession, telegram_id: int) -> list[int]:
    user = await session.get(
        User, {"telegram_id": telegram_id}, options=[selectinload(User.channels)]
    )
    
    return user.channels


async def get_users(
    session: AsyncSession,
    number_of_users: int,
) -> list[User]:
    stmt = (
        select(User)
        .order_by(User.first_name)
        .limit(number_of_users)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()
    users = cast(list[User], users)
    return users
