from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    hello: Hello
    start: Start
    button: Button
    no: No


class Hello:
    @staticmethod
    def admin(*, username) -> Literal["""Привет, { $username } 👋! Я могу:

📅 запланировать пост 📅
✍ Подготовить карточку товара по отправленной фотографии или тексту ✍

✨ Для демонстрации возможностей нажми &lt;code&gt;/demo&lt;/code&gt; ✨"""]: ...


class Start:
    @staticmethod
    def button() -> Literal["""Кнопка"""]: ...


class Button:
    @staticmethod
    def pressed() -> Literal["""Вы нажали на кнопку"""]: ...


class No:
    @staticmethod
    def handle() -> Literal["""Не смог обработать ваше сообщение.\nНажмите &lt;code&gt;/help&lt;/code&gt;, для просмотра доступных команд."""]: ...

