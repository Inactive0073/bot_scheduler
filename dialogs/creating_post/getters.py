from typing import TYPE_CHECKING, Dict

from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type:ignore


async def get_watch_text(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    return {
        "watch_text": i18n.cr.watch.text(),
    }


async def get_creating_post_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    content_msg = dialog_manager.dialog_data.get("post_message", "Message not found")
    return {
        "reply_title": i18n.cr.reply.text(),
        "post_message": content_msg,
        "edit": i18n.cr.edit.text(),
        "url": i18n.cr.url.btns(),
        "set_time": i18n.cr.set.time(),
        "set_notify": i18n.cr.set.notify(),
        "unset_notify": i18n.cr.unset.notify(),
        "media": i18n.cr.add.media(),
        "unset_comments": i18n.cr.unset.comments(),
        "push_now": i18n.cr.push.now(),
    }


async def get_url_instruction(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    return {
        "instruction_url": i18n.cr.instruction.url(),
    }
