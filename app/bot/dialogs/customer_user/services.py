from datetime import datetime as dt


def check_birthday_format(birthday: str) -> str:
    return dt.strptime(birthday, "%d.%m.%Y").strftime("%d.%m.%Y")
