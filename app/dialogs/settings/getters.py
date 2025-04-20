import datetime
from typing import TYPE_CHECKING, Dict

from aiogram.types import User

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Multiselect

from dataclasses import dataclass

from fluentogram import TranslatorRunner

from app.db.requests import  get_user_tz

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type:ignore


async def get_settings_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
) -> Dict[str, str]:
    return {
        "cancel_caption": i18n.cancel(),
        "yes_caption": i18n.yes(),
        "next": i18n.next(),
        "back": i18n.back(),
        "settings_support_message": i18n.settings.support.message(),
    }


async def get_setting_menu_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
) -> Dict[str, str]:
    return {
        "settings_menu_message": i18n.settings.main.menu(),
        "settings_timezone_button": i18n.settings.timezone.button(),
        "settings_support_button": i18n.settings.support.button(),
    }


async def get_start_setting_tz_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    session = dialog_manager.middleware_data.get("session")
    user_timezone = await get_user_tz(session=session, telegram_id=event_from_user.id)
    current_timezone = dialog_manager.dialog_data.get("user_timezone")
    selected_timezone = current_timezone if current_timezone else user_timezone
    local_time = datetime.datetime.now(selected_timezone).strftime("%H:%M")
    return {
        "settings_select_timezone_message": i18n.settings.select.timezone(
            current_timezone=selected_timezone, local_datetime=local_time
        ),
        "timezones": [
            ("Калининград", "Europe/Kaliningrad"),
            ("Москва", "Europe/Moscow"),
            ("Самара", "Europe/Samara"),
            ("Екатеринбург", "Asia/Yekaterinburg"),
            ("Омск", "Asia/Omsk"),
            ("Красноярск", "Asia/Krasnoyarsk"),
            ("Иркутск", "Asia/Irkutsk"),
            ("Якутск", "Asia/Yakutsk"),
            ("Владивосток", "Asia/Vladivostok"),
            ("Магадан", "Asia/Magadan"),
            ("Камчатка", "Asia/Kamchatka"),
        ],

    }
