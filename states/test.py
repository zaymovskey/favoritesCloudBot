from aiogram.dispatcher.filters.state import StatesGroup, State


class FolderState(StatesGroup):
    add_folder = State()
    delete_folder = State()
