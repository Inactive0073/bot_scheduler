from typing import TYPE_CHECKING, Dict

from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from app.bot.db.common_requests import get_user_role
from app.bot.utils.enums.role import UserType


if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type:ignore


async def get_common_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    web_app_url = dialog_manager.middleware_data.get("web_app_url")
    session = dialog_manager.middleware_data.get("session")
    is_admin = UserType.ADMIN in await get_user_role(
        session=session, telegram_id=event_from_user.id
    )
    return {
        "back": i18n.back(),
        "hello_waiter": i18n.waiter.hello.message(),
        "waiter_menu_scan": i18n.waiter.menu.scan(),
        "waiter_menu_scan_url": f"{web_app_url}/",
        "is_admin": is_admin,
        "to_admin_menu": i18n.admin.comeback.btn(),
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
