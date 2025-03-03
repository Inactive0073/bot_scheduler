from typing import List
from aiogram_dialog import Dialog

from app.dialogs.start.dialogs import start_dialog
from app.dialogs.creating_post.dialogs import create_post_dialog
from app.dialogs.addition_channel.dialogs import dialog_addition_channel


def get_dialogs() -> List[Dialog]:
    return [
        start_dialog,
        create_post_dialog,
        dialog_addition_channel,
    ]
