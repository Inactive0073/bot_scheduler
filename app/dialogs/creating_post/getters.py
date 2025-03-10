from typing import TYPE_CHECKING, Dict

from aiogram.types import User

from aiogram_dialog import DialogManager

from dataclasses import dataclass

from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type:ignore


@dataclass
class NotifyAlert:
    id: str
    desc: str


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
    content_msg = dialog_manager.dialog_data.get("post_message", "Сообщение не найдено")
    url_button_empty = dialog_manager.dialog_data.get("url_button_empty", True)

    posting_time = dialog_manager.dialog_data.get("dt_posting_view", None)
    posting_time_index = bool(posting_time)

    notify_status = dialog_manager.dialog_data.get("notify_status", True)

    return {
        "reply_title": i18n.cr.reply.text(),
        "post_message": content_msg,
        "edit": i18n.cr.edit.text(),
        "url": i18n.cr.url.btns(),
        "url_delete": i18n.cr.url.delete(),
        "set_time": i18n.cr.set.time(),
        "posting_time": posting_time,
        "posting_time_index": posting_time_index,
        "states_notify": [
            NotifyAlert(id="turn_on", desc=i18n.cr.set.notify()),
            NotifyAlert(id="turn_off", desc=i18n.cr.unset.notify()),
        ],
        "notify_status": notify_status,
        "media": i18n.cr.add.media(),
        "unset_comments": i18n.cr.unset.comments(),
        "push_now": i18n.cr.push.now(),
        "push_later": i18n.cr.push.later(),
        "url_button_empty": url_button_empty,
        "url_button_exists": not url_button_empty,
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


async def get_time_instruction_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    return {"instruction_delayed_post": i18n.cr.instruction.delayed.post()}


async def get_addition_media_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    return {
        "instruction_add_media": i18n.cr.instruction.media.post(),
    }
