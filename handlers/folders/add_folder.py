from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.folders.folders_moving import callback_string_to_int_or_none, get_user_folders_and_current_path
from loader import bot, dp
from services.folder_service import FolderService
from states import FolderState


@dp.callback_query_handler(FolderService.FOLDER_CB.filter(action="add_folder"))
async def create_folder_handler(
        callback_query: types.CallbackQuery, callback_data: dict
):
    await bot.send_message(callback_query.from_user.id, text="Введите название папки")
    await FolderState.add_folder.set()
    state = dp.get_current().current_state()
    await state.update_data(parent_id=callback_data.get('parent_id'))


@dp.message_handler(state=FolderState.add_folder)
async def add_folder(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()

    parent_id = callback_string_to_int_or_none(data.get('parent_id'))
    FolderService().add_folder(message.from_id, message.text, parent_id)

    user_folders_kb, current_folder_path = get_user_folders_and_current_path(
        message.from_id,
        parent_id
    )

    await bot.send_message(
        message.from_id,
        text=current_folder_path,
        reply_markup=user_folders_kb,
    )
