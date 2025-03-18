from typing import TYPE_CHECKING

from aiogram.types import User

from aiogram_dialog import DialogManager

from fluentogram import TranslatorRunner

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.requests import get_channels

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner


async def get_url_info(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str | bool]:
    session: AsyncSession = dialog_manager.middleware_data.get("session")

    channels = await get_channels(session=session, telegram_id=event_from_user.id)
    channel_exists = bool(channels)

    return {
        "channel_exists_message": i18n.channel.exists(),
        "channel_not_exists_message": i18n.channel._not.exists(),
        "instruction_add_channel": i18n.channel.instruction.add(),
        "url_button": i18n.channel.link.addition(),
        "url_button_name": i18n.channel.add.channel.button(),
        "channel_exists": channel_exists,
        "channels": channels,
    }
