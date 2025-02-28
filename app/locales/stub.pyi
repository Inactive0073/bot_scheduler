from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    start: Start
    cr: Cr
    channel: Channel

    @staticmethod
    def cancel() -> Literal["""❌Отмена"""]: ...


class Start:
    hello: StartHello
    create: StartCreate
    edit: StartEdit
    add: StartAdd

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


class StartAdd:
    @staticmethod
    def channel() -> Literal["""Мои каналы"""]: ...


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

    @staticmethod
    def later() -> Literal["""📅Запланировать пост"""]: ...


class CrInstruction:
    delayed: CrInstructionDelayed
    invalid: CrInstructionInvalid
    media: CrInstructionMedia

    @staticmethod
    def url() -> Literal["""⚠ Отправьте кнопки в формате:
Link - https://ya.ru | Link 2 - https://no.com
Link 3 - http://ac.ru | Link 4 - http://mail.ru

Каждую новую кнопку отправьте с новой строки.
Если хотите разместить несколько кнопок в одной строке используйте разделитель « | »"""]: ...


class CrInstructionDelayed:
    @staticmethod
    def post() -> Literal["""&lt;b&gt;Отправьте время выхода поста в часовом поясе (Europe/Moscow) в любом удобном формате, например:&lt;/b&gt;
&lt;blockquote&gt;
18 - текущие сутки 18:00
0830 - текущие сутки 08:30
08 30 - текущие сутки 08:30
1830 - текущие сутки 18:30
18300408 - 18:30 04.08
18 30 04 08 - 18:30 04.08
&lt;/blockquote&gt;"""]: ...


class CrInstructionInvalid:
    @staticmethod
    def time() -> Literal["""Не поддерживаю такой формат ввода данных 🤷‍♂️
&lt;b&gt;Отправьте время выхода поста в часовом поясе (Europe/Moscow) в любом удобном формате, например:&lt;/b&gt;
&lt;blockquote&gt;
18 - текущие сутки 18:00
0830 - текущие сутки 08:30
08 30 - текущие сутки 08:30
1830 - текущие сутки 18:30
18300408 - 18:30 04.08
18 30 04 08 - 18:30 04.08
&lt;/blockquote&gt;"""]: ...


class CrInstructionMedia:
    invalid: CrInstructionMediaInvalid

    @staticmethod
    def post() -> Literal["""📷 Пришлите медиа файлы"""]: ...

    @staticmethod
    def approve() -> Literal["""Все медиа файлы отправлены ❓"""]: ...

    @staticmethod
    def yes() -> Literal["""✅ Да"""]: ...

    @staticmethod
    def no() -> Literal["""❌ Нет"""]: ...


class CrInstructionMediaInvalid:
    @staticmethod
    def type() -> Literal["""❌ Не поддерживаю такой тип данных ❌  
Допустимые форматы:
- Фото
- Видео

Для демонстрации бота нажмите /demo или напишите в &lt;a href=&#34;@inactive0073&#34;&gt;поддержку бота&lt;/a&gt;"""]: ...


class Channel:
    instruction: ChannelInstruction


class ChannelInstruction:
    @staticmethod
    def add() -> Literal["""Ниже представлен список ваших каналов.
Для добавления бота сделайте бота администратором в канале и дайте ему права на управление сообщениями и управление историями."""]: ...

