from typing import List
from aiogram_dialog import Dialog

from dialogs.start.dialogs import start_dialog, create_post_dialog

def get_dialogs() -> List[Dialog]:
    return [
        start_dialog,
        create_post_dialog,
    ]