from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from sqlalchemy import and_, select, ChunkedIteratorResult
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.collections import InstrumentedList

from database import session
from keyboards.folders_footer_ik import get_folders_footer_ik
from models import Folder


class FolderService:
    FOLDER_CB = CallbackData("folder", "action", "folder_id", "parent_id")

    def __init__(self):
        self.session = session

    def get_folder_path(self, user_id: int, folder_id: int = None) -> str:
        """Получение пути до папки"""

        stmt = select(Folder.id, Folder.parent_id, Folder.name).where(
            Folder.user_id == user_id
        )
        user_folders = self.session.execute(stmt)
        path_array = self.create_path(user_folders, folder_id).split("/")
        """ Переписать, чтобы не надо было вот эту хуйню с remove писать """
        path_array.remove("")
        path_array.reverse()
        path = "/".join([str(folder) for folder in path_array])
        path = path if path else "/"
        return path

    def get_user_folders_kb(
        self, user_id: int, folder_id: int = None, parent_id: int = None
    ) -> InlineKeyboardMarkup:
        """Получение инлайн-кнопок с папками"""

        stmt = self.session.query(Folder).where(
            and_(Folder.user_id == user_id, Folder.parent_id == folder_id)
        )
        try:
            folders = self.session.scalars(stmt)
            user_folders_kb = self.create_user_folders_kb(folders)
            user_folders_kb.extend(
                get_folders_footer_ik(
                    self.FOLDER_CB.new(
                        action="to_folder",
                        folder_id=str(parent_id),
                        parent_id="None",
                    )
                )
            )
            user_folders_kb = InlineKeyboardMarkup(
                row_width=4, inline_keyboard=user_folders_kb
            )
            return user_folders_kb
        except NoResultFound:
            pass

    def create_path(
        self, user_folders: ChunkedIteratorResult, folder_id: int | None
    ) -> str:
        """Создание пути в виде списка имен папок на основе всех папок пользователя"""

        path = "/"
        for folder in user_folders:
            if folder[0] == folder_id:
                path = path + folder[2]
                path = path + self.create_path(user_folders, folder[1])
        return path

    def create_user_folders_kb(self, folders: InstrumentedList) -> list:
        """Генерация сетки инлайн-кнопок папок"""

        folders_kb = []
        row = []
        for folder in folders:
            button = InlineKeyboardButton(
                text=folder.name,
                callback_data=self.FOLDER_CB.new(
                    action="to_folder",
                    folder_id=folder.id,
                    parent_id=str(folder.parent_id),
                ),
            )
            row.append(button)
            if len(row) == 4:
                folders_kb.append(row.copy())
                row.clear()
        folders_kb.append(row)
        return folders_kb
