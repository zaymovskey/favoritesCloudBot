from loader import dp, bot
from aiogram import types
from services.folder_service import FolderService


def callback_string_to_int_or_none(value) -> int | None:
    return int(value) if value != "None" else None


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_folders_kb = FolderService().get_user_folders_kb(message.from_id)
    current_folder_path = FolderService().get_folder_path(message.from_id)
    await message.answer(text=current_folder_path, reply_markup=user_folders_kb)


@dp.callback_query_handler(FolderService.FOLDER_CB.filter(action="to_folder"))
async def go_to_folder_handler(
    callback_query: types.CallbackQuery, callback_data: dict
):
    folder_id = callback_string_to_int_or_none(callback_data.get("folder_id"))
    parent_id = callback_string_to_int_or_none(callback_data.get("parent_id"))

    user_folders_kb = FolderService().get_user_folders_kb(
        callback_query.from_user.id,
        folder_id,
        parent_id,
    )
    current_folder_path = FolderService().get_folder_path(
        callback_query.from_user.id, folder_id
    )

    await bot.send_message(
        callback_query.from_user.id,
        text=current_folder_path,
        reply_markup=user_folders_kb,
    )
