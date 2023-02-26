from database import session
from loader import dp
from aiogram import types
from services.folder_service import FolderService


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_folders_kb = FolderService(session).get_user_folders_kb(message.from_id)
    current_folder_path = FolderService(session).get_current_folder_path(
        message.from_id
    )
    await message.answer(text=current_folder_path, reply_markup=user_folders_kb)
