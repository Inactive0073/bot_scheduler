from validators.url import url


def validate_button_case(text: str) -> bool:
    """
    Валидатор корректного сообщения пользователя
    """
    res = url(text)
    if res:
        return res
    raise ValueError(res)
