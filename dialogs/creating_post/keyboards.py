from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dialogs.creating_post.filters import validate_button_case
from dialogs.creating_post.services import parse_button


def create_keyboard_for_url(text: str) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру на основе текстового описания кнопок.

    Параметры:
        text (str): Текст в формате:
            Кнопка1 - https://url1 | Кнопка2 - https://url2
            НоваяСтрокаКнопок - https://url3

    Возвращает:
        InlineKeyboardMarkup: Объект клавиатуры для Telegram

    """
    builder = InlineKeyboardBuilder()

    for row in text.strip().split("\n"):
        for el in row.split("|"):
            row_buttons = []
            name, link = parse_button(el)
            if validate_button_case(link):
                button = InlineKeyboardButton(text=name, url=link)
            row_buttons.append(button)
            builder.row(*row_buttons)

    keyboard = builder.as_markup()
    return keyboard
