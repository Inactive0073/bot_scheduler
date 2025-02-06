from typing import TYPE_CHECKING

from aiogram.types import Message, InlineKeyboardMarkup
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput, TextInput

from states.creating_post import PostingSG

from logging import getLogger

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type: ignore

logger = getLogger(__name__)


async def process_post_msg(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    """Обработчик сообщения с постом пользователя.
    Сохраняет сообщение в dialog_data для дальнейшей репрезентации пользователю
    и осуществляет переход в следующее окно.
    """
    copy_msg = await message.send_copy(chat_id=message.chat.id)
    logger.debug(
        f"Полученые следующие данные:"
        f"message_id={copy_msg.message_id} \n{copy_msg.chat.id=}\ntext={copy_msg.text}\n"
    )
    # удаляем старое сообщение, чтобы сохранить историю чище
    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=message.message_id
    )

    dialog_manager.dialog_data.update(
        {
            "post_message": copy_msg.text,
            "chat_id": copy_msg.chat.id,
            "message_id": copy_msg.message_id,
        }
    )
    await dialog_manager.switch_to(
        state=PostingSG.creating_post, show_mode=ShowMode.DELETE_AND_SEND
    )


async def process_other_type_msg(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    """
    Обрабатывает сообщения с неподдерживаемыми типами контента.

    Отправляет пользователю сообщение о недопустимом формате данных.
    Используется для фильтрации нежелательных типов ввода (не текст/фото).
    """
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    await message.answer(i18n.cr.invalid.data())


async def process_button_case(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    keyboard: InlineKeyboardMarkup,
) -> None:
    """
    Обрабатывает ввод пользователя для добавления URL-кнопок к сообщению.

    Обновляет исходное сообщение, добавляя к нему инлайн-клавиатуру.
    Использует данные из dialog_data для редактирования сообщения.

    Логирует процесс формирования клавиатуры и результат редактирования.
    """
    # Получаем данные из dialog_data для создания кнопки
    msg_id = dialog_manager.dialog_data["message_id"]
    chat_id = dialog_manager.dialog_data["chat_id"]
    post_message = dialog_manager.dialog_data["post_message"]
    
    # Кладем клавиатуру в dialog_data
    dialog_manager.dialog_data['keyboard'] = keyboard

    # добавляем сообщению кнопки
    await message.bot.edit_message_text(
        text=post_message, chat_id=chat_id, message_id=msg_id, reply_markup=keyboard
    )

    # удаляем старое сообщение для чистой истории
    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=message.message_id
    )

    logger.debug("Сообщение было отредактировано")
    await dialog_manager.switch_to(PostingSG.creating_post, ShowMode.DELETE_AND_SEND)


async def process_invalid_button_case(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    """
    Удаляет сообщения с неудачным текстом и инструкцией для чистой истории
    """
    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=message.message_id - 1
    )
    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=message.message_id
    )


async def edit_text(
        message: Message,
        widget: TextInput,
        dialog_manager: DialogManager,
        text: str
):
    # получаем данные для редактирования сообщения
    msg_id = dialog_manager.dialog_data["message_id"]
    chat_id = dialog_manager.dialog_data["chat_id"]

    keyboard = dialog_manager.dialog_data.get("keyboard")

    # удаляем старое сообщение
    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    # редактируем выбранное сообщение
    if keyboard:
        await message.bot.edit_message_text(
            text=text,
            message_id=msg_id,
            chat_id=chat_id,
            reply_markup=keyboard
        )

    else:
        await message.bot.edit_message_text(
            text=text,
            message_id=msg_id,
            chat_id=chat_id,
        )

    # Возвращаемся обратно в меню создания и настройки поста
    await dialog_manager.switch_to(PostingSG.creating_post, show_mode=ShowMode.DELETE_AND_SEND)