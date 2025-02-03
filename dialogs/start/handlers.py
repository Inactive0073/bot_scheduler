from typing import TYPE_CHECKING

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput

from states.start import PostingSG

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner # type: ignore

    
async def process_post_msg(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager
) -> None:
    '''Обработчик нажатия кнопки Создать пост. 
    Сохраняет сообщение в dialog_data для дальнейшей репрезентации пользователю 
    и осуществляет переход в следующий диалог.
    '''
    dialog_manager.dialog_data['post_message'] = message.text
    await dialog_manager.start(state=PostingSG.creating_post)


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

