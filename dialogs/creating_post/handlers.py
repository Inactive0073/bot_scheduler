from typing import TYPE_CHECKING

from aiogram.types import Message, InlineKeyboardMarkup
from aiogram_dialog import DialogManager
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
    dialog_manager.dialog_data.update(
        {
            "post_message": message.text,
            "chat_id": message.chat.id,
            "message_id": message.message_id,
        }
    )
    await dialog_manager.switch_to(state=PostingSG.creating_post)


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
    message: Message, widget: TextInput, dialog_manager: DialogManager, keyboard: InlineKeyboardMarkup
) -> None:
    """
    Обрабатывает ввод пользователя для добавления URL-кнопок к сообщению.

    Обновляет исходное сообщение, добавляя к нему инлайн-клавиатуру.
    Использует данные из dialog_data для редактирования сообщения.

    Логирует процесс формирования клавиатуры и результат редактирования.
    """
    # Получаем данные из dialog_data для обновления кнопки
    msg_id = dialog_manager.dialog_data["message_id"]
    chat_id = dialog_manager.dialog_data["chat_id"]
    post_message = dialog_manager.dialog_data["post_message"]

    logger.debug(
        f"Полученые следующие данные:"
        f"message_id={msg_id} \n{chat_id=}\ntext={post_message}\n"
        f"Начали формировать клавиатуру..."
    )
    # формируем юзер-клавиатуру

    logger.debug(f"Клавиатура сформирована. Текущий объект клавиатуры: {keyboard}")

    # добавляем сообщению кнопки
    await message.bot.edit_message_reply_markup(
        chat_id=chat_id, 
        message_id=msg_id, 
        reply_markup=keyboard
    )
    logger.debug("Сообщение было отредактировано")


async def process_invalid_button_case(
    message: Message, widget: TextInput, dialog_manager: DialogManager, err: ValueError
) -> None:
    """
    Обработка невалидного сообщения.
    """
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    logger.info(f"Не валидная ссылка, произошла ошибка:\n{err}")
    await message.answer(i18n.cr.instruction.url())
