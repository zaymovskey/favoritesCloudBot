from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from sqlalchemy import and_, select, delete
from sqlalchemy.exc import NoResultFound

from database import session
from keyboards.folders_footer_ik import get_folders_footer_ik
from models import Folder


class FolderService:
    FOLDER_CB = CallbackData("folder", "action", "folder_id", "parent_id")

    FOLDERS_KEYBOARD_WIDTH = 4

    def __init__(self):
        self.session = session

    def add_folder(self, user_id: int, folder_name: str, parent_id: int = None) -> None:
        """Добавление папки"""

        new_folder = Folder(user_id=user_id, name=folder_name, parent_id=parent_id)
        self.session.add(new_folder)
        self.session.commit()

    def get_folder_path(self, user_id: int, folder_id: int = None) -> str:
        """Получение пути до папки"""

        stmt = select(Folder.id, Folder.parent_id, Folder.name).where(
            Folder.user_id == user_id
        )
        user_folders = self.session.execute(stmt).fetchall()
        path_array = self.create_folder_path(user_folders, folder_id).split("/")
        path_array.remove("")
        path_array.reverse()
        path = "/".join([str(folder) for folder in path_array])
        path = path if path else "/"
        return path

    def get_user_folders_kb(
        self,
        user_id: int,
        folder_id: int = None,
        parent_id: int = None,
        with_footer: bool = True,
    ) -> InlineKeyboardMarkup:
        """Получение инлайн-кнопок с папками"""

        stmt = (
            select(Folder.id, Folder.name, Folder.parent_id)
            .where(and_(Folder.user_id == user_id, Folder.parent_id == folder_id))
            .order_by(Folder.name)
        )
        try:
            folders = self.session.execute(stmt).fetchall()
            user_folders_kb = self.create_user_folders_kb(folders)
            if with_footer:
                user_folders_kb.extend(
                    get_folders_footer_ik(
                        back_callback_data=self.FOLDER_CB.new(
                            action="to_folder",
                            # id родительской папки, чтобы перейти в нее как в обычную
                            folder_id=str(parent_id),
                            parent_id="None",
                        ),
                        add_folder_callback_data=self.FOLDER_CB.new(
                            action="add_folder",
                            # id текущей папки, чтобы потом занести ее в parent_id новой и показать содержимое текущей
                            folder_id=str(folder_id),
                            parent_id="None",
                        ),
                        delete_folder_callback_data=self.FOLDER_CB.new(
                            action="delete_folder",
                            # id текущей папки, чтобы после удаления показать нужную
                            folder_id=str(folder_id),
                            parent_id="None",
                        ),
                    )
                )
            user_folders_kb = InlineKeyboardMarkup(
                row_width=4, inline_keyboard=user_folders_kb
            )
            return user_folders_kb
        except NoResultFound:
            pass

    def delete_folder(self, folder_id: int):
        stmt = delete(Folder).where(Folder.id == folder_id)
        self.session.execute(stmt)
        self.session.commit()

    def create_folder_path(
        self, user_folders: list[Folder], folder_id: int | None
    ) -> str:
        """Создание пути до папки на основе всех папок пользователя"""

        path = "/"
        for folder in user_folders:
            if folder.id == folder_id:
                path = path + folder.name
                path = path + self.create_folder_path(user_folders, folder.parent_id)
        return path

    def create_user_folders_kb(self, folders: list[Folder]) -> list:
        """Генерация сетки инлайн-кнопок папок"""

        folders_kb = []
        row = []
        for folder in folders:
            button = InlineKeyboardButton(
                text=folder.name + " 📁",
                callback_data=self.FOLDER_CB.new(
                    action="to_folder",
                    folder_id=folder.id,
                    parent_id=str(folder.parent_id),
                ),
            )
            row.append(button)
            if len(row) == self.FOLDERS_KEYBOARD_WIDTH:
                folders_kb.append(row.copy())
                row.clear()
        folders_kb.append(row)
        return folders_kb
