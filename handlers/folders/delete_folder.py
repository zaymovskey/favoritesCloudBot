from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.folders.folders_moving import (
    get_user_folders_and_current_path,
    callback_string_to_int_or_none,
)
from loader import dp, bot
from services.folder_service import FolderService
from states import FolderState


@dp.callback_query_handler(FolderService.FOLDER_CB.filter(action="delete_folder"))
async def set_delete_folder_state(
    callback_query: types.CallbackQuery, callback_data: dict
):
    folders_ik = FolderService().get_user_folders_kb(
        user_id=callback_query.from_user.id,
        folder_id=callback_string_to_int_or_none(callback_data.get("parent_id")),
        with_footer=False,
    )
    await bot.send_message(
        callback_query.from_user.id,
        text="Выберите папку, которую хотите удалить",
        reply_markup=folders_ik,
    )

    await FolderState.delete_folder.set()


@dp.callback_query_handler(state=FolderState.delete_folder)
async def delete_folder(callback_query: types.CallbackQuery, state: FSMContext):
    callback_data = callback_query.data.split(":")
    folder_id = int(callback_data[2])
    FolderService().delete_folder(folder_id)
    await state.finish()
    parent_id = callback_string_to_int_or_none(callback_data[3])

    user_folders_kb, current_folder_path = get_user_folders_and_current_path(
        callback_query.from_user.id, parent_id
    )

    await bot.send_message(
        callback_query.from_user.id,
        text=current_folder_path,
        reply_markup=user_folders_kb,
    )
