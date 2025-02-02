from typing import TYPE_CHECKING, Dict

from aiogram import html
from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner # type:ignore 

async def get_hello(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs,
) -> Dict[str, str]:
    username = html.quote(event_from_user.first_name if event_from_user.first_name else "пользователь") 
    return {"hello_admin": i18n.hello.admin(username=username),
            "start_button": i18n.start.button()}