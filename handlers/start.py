from database import session
from loader import dp
from aiogram import types
from services.folder_service import FolderService


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_folders_kb = FolderService(session, message).get_user_folders_kb()
    await message.answer(text="/", reply_markup=user_folders_kb)
