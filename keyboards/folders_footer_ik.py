from aiogram.types import InlineKeyboardButton


def get_folders_footer_ik(
    back_callback_data: str, add_folder_callback_data: str
) -> list:
    folders_footer_ik = [
        [
            InlineKeyboardButton(
                text="Создать папку ➕", callback_data=add_folder_callback_data
            ),
            InlineKeyboardButton(text="Назад ⬅️", callback_data=back_callback_data),
        ],
        [
            InlineKeyboardButton(
                text="Удалить текущую директорию ❌", callback_data="fdsfsd"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Файлы текущей директории 📋", callback_data="fdsaf"
            ),
        ],
    ]
    return folders_footer_ik
