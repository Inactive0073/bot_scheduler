from typing import TYPE_CHECKING, Dict

from aiogram import html
from aiogram.types import User
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
        "waiter_menu_scan_url": f"{web_app_url}/scan",
    }
