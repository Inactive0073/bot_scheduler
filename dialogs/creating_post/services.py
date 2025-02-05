from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import Tuple
from validators.url import url

def parse_button(text: str) -> InlineKeyboardMarkup:
    """
    Парсит текст для создания Inline-клавиатуры с кнопками.

    Формат текста:
        Каждая строка — ряд кнопок. Элементы в строке разделены через "|".
        Каждая кнопка задается в формате: "Текст кнопки - URL".

    Пример:
        "Кнопка 1 - https://ya.ru | Кнопка 2 - https://google.com"

    Args:
        text (str): Входной текст с описанием кнопок.

    Returns:
        InlineKeyboardMarkup: Объект клавиатуры с кнопками.

    Raises:
        ValueError: 
            - Если формат строки кнопки некорректен (не разделено на "Текст - URL").
            - Если URL не проходит валидацию.
    """
    builder = InlineKeyboardBuilder()

    for row in text.strip().split("\n"):
        row_buttons = []
        for el in row.split("|"):
            parts = [p for p in el.split(" - ")]

            if len(parts) != 2:
                raise ValueError(
                    f"Некорректный формат кнопки.\n"
                    f"Образец ссылки: Example link - https://ya.ru\n"
                    f"Получено: {''.join(parts)}\n"
                )
            name, link = parts

            if not url(link):
                raise ValueError(
                    f"Ошибка в процессе валидации ссылки, проверьте ссылку: {link}"
                )

            row_buttons.append(InlineKeyboardButton(text=name, url=link))

        builder.row(*row_buttons)
    
    return builder.as_markup()