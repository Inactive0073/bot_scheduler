from typing import TYPE_CHECKING
from aiogram.types import User

from aiogram_dialog import DialogManager

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

async def get_main_info(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User
) -> dict[str, str]:
    return {
        "instruction_add_channel": i18n.channel.instruction.add(),
        "url_button": i18n.channel.link.addition(),
    }