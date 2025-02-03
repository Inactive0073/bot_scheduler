from typing import TYPE_CHECKING

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.api.internal import ReplyCallbackQuery

from states.start import StartSG

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner # type: ignore

    # i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    
async def create_post_click(
        cb: ReplyCallbackQuery,
        button: SwitchTo,
        dialog_manager: DialogManager
) -> None:
    msg = cb.original_message
    await msg.bot.delete_message(
        chat_id=msg.chat.id,
        message_id=msg.message_id
    )
    dialog_manager.dialog_data['msg_to_reply'] = msg # Кладем старое сообщение в хранилище для дальнейшего использования
    
    
async def edit_post_click(
    message: Message,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    pass

async def create_description_click(
    message: Message,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    pass

async def settings_click(
    message: Message,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    pass

