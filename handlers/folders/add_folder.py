from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import bot, dp
from services.folder_service import FolderService
from states import FolderState


@dp.callback_query_handler(text="create_folder")
async def create_folder_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, text="Введите название папки")
    await FolderState.add_folder.set()


@dp.message_handler(state=FolderState.add_folder)
async def add_folder(message: types.Message, state: FSMContext):
    await state.finish()
    FolderService().add_folder(message.from_id, message.text)
