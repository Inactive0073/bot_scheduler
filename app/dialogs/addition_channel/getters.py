from typing import TYPE_CHECKING
from aiogram.types import User

from aiogram_dialog import DialogManager

from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

async def get_url_info(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs
) -> dict[str, str]:
    return {
        "channel_exists": i18n.channel.exists(),
        "channel_exists": i18n.channel._not.exists(),
        "instruction_add_channel": i18n.channel.instruction.add(),
        "url_button": i18n.channel.link.addition(),
    }