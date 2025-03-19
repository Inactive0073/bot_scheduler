from typing import TYPE_CHECKING

from aiogram.types import User

from aiogram_dialog import DialogManager

from fluentogram import TranslatorRunner

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.requests import get_channels, get_channel

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


async def get_channel_settings(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    session: AsyncSession = dialog_manager.middleware_data.get("session")

    channel = await get_channel(
        session=session, channel_id=dialog_manager.dialog_data["channel_selected_id"]
    )
    name = channel.channel_name
    caption = channel.channel_caption if channel.channel_caption else i18n.no()
    channel_settings_desc = i18n.channel.settings.desc(name=name, caption=caption)
    print(f"{channel.__dict__=}")

    return {
        "channel_name": name,
        "channel_caption": caption,
        "channel_settings_desc": channel_settings_desc,
        "channel_delete_from_bot_desc": i18n.channel.delete._from.bot(),
        "channel_add_caption_desc": i18n.channel.add.caption(),
    }


async def get_data_for_delete(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "delete_bot_from_channel_desc": i18n.channel.delete.channel.instruction(),
        "channe_delete_button": i18n.channel.delete.button(),
    }
