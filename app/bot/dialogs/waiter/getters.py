from typing import TYPE_CHECKING, Dict

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type:ignore


async def get_common_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
) -> Dict[str, str]:
    web_app_url = dialog_manager.middleware_data.get("web_app_url")
    return {
        "back": i18n.back(),
        "hello_waiter": i18n.waiter.hello.message(),
        "waiter_menu_scan": i18n.waiter.menu.scan(),
        "waiter_menu_scan_url": f"{web_app_url}/",
    }


async def get_processing_guest_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
) -> Dict[str, str]:
    return {
        "process_guest_message": i18n.waiter.processing.instruction(),
        "add_bonus_button": i18n.waiter.processing.add.bonus(),
        "subtract_bonus_button": i18n.waiter.processing.subtract.bonus(),
        "adding_instruction": i18n.waiter.processing.adding.bonus.instruction(),
        "subtracting_instruction": i18n.waiter.processing.subtracting.instruction(),
    }
