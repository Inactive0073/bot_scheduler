from typing import TYPE_CHECKING, Dict

from aiogram import html
from aiogram.types import User, Message
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
    return {
        "hello_admin": i18n.start.hello.admin(username=username),
        "create_post": i18n.start.create.post(),
        "edit_post": i18n.start.edit.post(),
        "create_description": i18n.start.create.description(),
        "settings": i18n.start.settings(),
        }
    
async def get_creating_post_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User
) -> Dict[str, str]:
    msg: Message = dialog_manager.dialog_data['msg_to_reply']
    return {
        'reply_title': i18n.cr.reply.text(),
        'msg_to_reply': msg.text,
        'edit': i18n.cr.edit.text(),
        'url': i18n.cr.url.btns(),
        'set_time': i18n.cr.set.time(),
        'set_notify': i18n.cr.set.notify(),
        'unset_notify': i18n.cr.unset.notify(),
        'media': i18n.cr.add.media(),
        'unset_comments': i18n.cr.unset.comments(),
        'push_now': i18n.cr.push.now()
        }