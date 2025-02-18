from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    start: Start
    cr: Cr

    @staticmethod
    def cancel() -> Literal["""❌Отмена"""]: ...


class Start:
    hello: StartHello
    create: StartCreate
    edit: StartEdit

    @staticmethod
    def settings() -> Literal["""Настройки"""]: ...


class StartHello:
    @staticmethod
    def admin(*, username) -> Literal["""Привет, { $username }👋

Я могу:
✍Составить описание товара✍
📅Запланировать пост📅
✍Подготовить карточку товара✍

✨Для демонстрации возможностей нажми /demo ✨"""]: ...


class StartCreate:
    @staticmethod
    def post() -> Literal["""Создать пост"""]: ...

    @staticmethod
    def description() -> Literal["""Создать описание"""]: ...


class StartEdit:
    @staticmethod
    def post() -> Literal["""Редактировать пост"""]: ...


class Cr:
    watch: CrWatch
    invalid: CrInvalid
    reply: CrReply
    edit: CrEdit
    url: CrUrl
    set: CrSet
    unset: CrUnset
    add: CrAdd
    push: CrPush
    instruction: CrInstruction


class CrWatch:
    @staticmethod
    def text() -> Literal["""✍ Отправьте текст поста, который необходимо опубликовать"""]: ...


class CrInvalid:
    @staticmethod
    def data() -> Literal["""❌ Не поддерживаю такой тип данных ❌  

Для демонстрации бота нажмите /demo или напишите в поддержку бота"""]: ...


class CrReply:
    @staticmethod
    def text() -> Literal["""👆 Проверьте текст, перед публикацей"""]: ...


class CrEdit:
    @staticmethod
    def text() -> Literal["""✍Изменить текст"""]: ...


class CrUrl:
    @staticmethod
    def btns() -> Literal["""☑️URL Кнопки"""]: ...

    @staticmethod
    def delete() -> Literal["""❌ Удалить кнопки"""]: ...


class CrSet:
    @staticmethod
    def time() -> Literal["""🕙Время отправки"""]: ...

    @staticmethod
    def notify() -> Literal["""🔔С уведомлением"""]: ...


class CrUnset:
    @staticmethod
    def notify() -> Literal["""🔕Без уведомления"""]: ...

    @staticmethod
    def comments() -> Literal["""☑️Отключить комментарии"""]: ...


class CrAdd:
    @staticmethod
    def media() -> Literal["""➕Добавить медиа"""]: ...


class CrPush:
    @staticmethod
    def now() -> Literal["""🚀Отправить сейчас"""]: ...


class CrInstruction:
    @staticmethod
    def url() -> Literal["""⚠ Отправьте кнопки в формате:
Link - https://ya.ru | Link 2 - https://no.com
Link 3 - http://ac.ru | Link 4 - http://mail.ru

Каждую новую кнопку отправьте с новой строки.
Если хотите разместить несколько кнопок в одной строке используйте разделитель « | »"""]: ...

