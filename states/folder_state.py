from aiogram.dispatcher.filters.state import StatesGroup, State


class FolderState(StatesGroup):
    add_folder = State()
    confirm_delete = State()
    delete_confirmed = State()
    delete_folder = State()
