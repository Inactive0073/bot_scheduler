from typing import List
from aiogram_dialog import Dialog

from .start.dialogs import start_dialog
from .creating_post.dialogs import create_post_dialog
from .addition_channel.dialogs import dialog_addition_channel
from .settings.dialogs import settings_dialog


def get_dialogs() -> List[Dialog]:
    return [start_dialog, create_post_dialog, dialog_addition_channel, settings_dialog]
