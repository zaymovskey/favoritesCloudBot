from loader import dp, bot
from aiogram import types
from services.folder_service import FolderService
from services.user_service import UserService


def callback_string_to_int_or_none(value) -> int | None:
    return int(value) if value not in ["None", None] else None


def get_user_folders_and_current_path(
    user_id: int, folder_id: int | str = None, parent_id: int | str = None
):
    folder_id = callback_string_to_int_or_none(folder_id)
    parent_id = callback_string_to_int_or_none(parent_id)

    folder_service = FolderService()

    user_folders_kb = folder_service.get_user_folders_kb(
        user_id=user_id,
        folder_id=folder_id,
        parent_id=parent_id,
    )

    current_folder_path = folder_service.get_folder_path(user_id, folder_id)

    return user_folders_kb, current_folder_path


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    UserService().add_user_if_not_exists(message.from_id)

    user_folders_kb, current_folder_path = get_user_folders_and_current_path(
        user_id=message.from_id
    )
    await message.answer(text=current_folder_path, reply_markup=user_folders_kb)


@dp.callback_query_handler(FolderService.FOLDER_CB.filter(action="to_folder"))
async def go_to_folder_handler(
    callback_query: types.CallbackQuery, callback_data: dict
):
    user_folders_kb, current_folder_path = get_user_folders_and_current_path(
        user_id=callback_query.from_user.id,
        folder_id=callback_data.get("folder_id"),
        parent_id=callback_data.get("parent_id"),
    )

    await bot.send_message(
        callback_query.from_user.id,
        text=current_folder_path,
        reply_markup=user_folders_kb,
    )
