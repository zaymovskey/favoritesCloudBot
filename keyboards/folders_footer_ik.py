from aiogram.types import InlineKeyboardButton


def get_folders_footer_ik(back_callback_data: str) -> list:
    folders_footer_ik = [
        [
            InlineKeyboardButton(text="Создать папку", callback_data="fdsaf"),
            InlineKeyboardButton(text="Назад", callback_data=back_callback_data),
        ],
        [
            InlineKeyboardButton(
                text="Файлы текущей директории", callback_data="fdsaf"
            ),
        ],
    ]
    return folders_footer_ik
