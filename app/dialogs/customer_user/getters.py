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
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    return {
        "back": i18n.back(),
        "hello_guest": i18n.customer.hello.message(),
        "meeting_phone_message": i18n.customer.meeting.phone(),
        "meeting_name_message": i18n.customer.meeting.name(),
        "meeting_surname_message": i18n.customer.meeting.surname(),
        "meeting_email_message": i18n.customer.meeting.email(),
        "meeting_birthday_message": i18n.customer.meeting.birthday(),
        "meeting_gender_message": i18n.customer.meeting.gender(),
        "meeting_gender_m_button": i18n.customer.meeting.gender.m(),
        "meeting_gender_f_button": i18n.customer.meeting.gender.f(),
        "meeting_thanks_message": i18n.customer.meeting.thanks(),
    }
