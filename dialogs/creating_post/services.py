from typing import Tuple


def parse_button(text: str) -> Tuple[str, str]:
    """
    Возвращает:
    Кортеж с двумя переменными. Именем кнопки и ссылкой

    Исключения:
        ValueError: При некорректном формате описания кнопки
    """
    parts = [p for p in text.split(" - ")]
    if len(parts) != 2:
        raise ValueError(
            f"Ссылка передана в некорректном виде."
            f"Образец ссылки: Example link - https://ya.ru"
            f"Была передана ссылка вида: {''.join(parts)}"
        )
