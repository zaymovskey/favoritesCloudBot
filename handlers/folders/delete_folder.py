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
async def set_delete_folder_state_handler(
        callback_query: types.CallbackQuery, callback_data: dict
):
    folders_ik = FolderService().get_user_folders_kb(
        user_id=callback_query.from_user.id,
        folder_id=callback_string_to_int_or_none(callback_data.get("folder_id")),
        with_footer=False,
    )
    await bot.send_message(
        callback_query.from_user.id,
        text="Выберите папку, которую хотите удалить",
        reply_markup=folders_ik,
    )

    await FolderState.confirm_delete.set()


@dp.callback_query_handler(state=FolderState.confirm_delete)
async def confirm_delete_folder_handler(
        callback_query: types.CallbackQuery, state: FSMContext
):
    callback_data = callback_query.data.split(":")
    deleting_folder_id = int(callback_data[2])
    folder_id = callback_string_to_int_or_none(callback_data[3])

    await state.update_data(deleting_folder_id=deleting_folder_id, folder_id=folder_id)

    await bot.send_message(
        callback_query.from_user.id,
        text="Вы уверены? (Все дочерние дочерние папки и файлы этой директории будут удалены) \nНапишите 'Да', "
             "если уверены.",
    )

    await FolderState.delete_confirmed.set()


@dp.message_handler(state=FolderState.delete_confirmed)
async def delete_folder_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    FolderService().delete_folder(data.get('deleting_folder_id'))

    user_folders_kb, current_folder_path = get_user_folders_and_current_path(
        user_id=message.from_user.id, folder_id=data.get('folder_od')
    )

    await bot.send_message(
        message.from_user.id,
        text=current_folder_path,
        reply_markup=user_folders_kb,
    )

