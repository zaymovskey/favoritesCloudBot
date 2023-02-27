from aiogram.dispatcher import FSMContext

from loader import dp, bot
from aiogram import types
from services.folder_service import FolderService
from states import FolderState


def callback_string_to_int_or_none(value) -> int | None:
    return int(value) if value not in ["None", None] else None


def get_user_folders_and_current_path(
    user_id: int, folder_id: int | str = None, parent_id: int | str = None
):
    folder_id = callback_string_to_int_or_none(folder_id)
    parent_id = callback_string_to_int_or_none(parent_id)

    folder_service = FolderService()

    user_folders_kb = folder_service.get_user_folders_kb(
        user_id,
        folder_id,
        parent_id,
    )

    current_folder_path = folder_service.get_folder_path(user_id, folder_id)

    return user_folders_kb, current_folder_path


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_folders_kb, current_folder_path = get_user_folders_and_current_path(
        message.from_id
    )
    await message.answer(text=current_folder_path, reply_markup=user_folders_kb)


@dp.callback_query_handler(FolderService.FOLDER_CB.filter(action="to_folder"))
async def go_to_folder_handler(
    callback_query: types.CallbackQuery, callback_data: dict
):
    user_folders_kb, current_folder_path = get_user_folders_and_current_path(
        callback_query.from_user.id,
        callback_data.get("folder_id"),
        callback_data.get("parent_id"),
    )

    await bot.send_message(
        callback_query.from_user.id,
        text=current_folder_path,
        reply_markup=user_folders_kb,
    )


@dp.callback_query_handler(text="create_folder")
async def create_folder_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, text="Введите название папки")
    await FolderState.add_folder.set()


@dp.message_handler(state=FolderState.add_folder)
async def add_folder(message: types.Message, state: FSMContext):
    await state.finish()
    FolderService().add_folder(message.from_id, message.text)
