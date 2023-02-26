from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.collections import InstrumentedList

from database import Session
from keyboards.folders_footer_ik import folders_footer_ik
from models import User


class FolderService:
    def __init__(self, session: Session):
        self.session = session

    def get_user_folders_kb(self, user_id: int) -> InlineKeyboardMarkup:
        stmt = self.session.query(User).where(User.user_id == user_id)
        try:
            current_user = self.session.scalars(stmt).one()
            user_folders_kb = self.create_user_folders_kb(current_user.folders)
            user_folders_kb.extend(folders_footer_ik)
            user_folders_kb = InlineKeyboardMarkup(
                row_width=4, inline_keyboard=user_folders_kb
            )
            return user_folders_kb
        except NoResultFound:
            pass

    @staticmethod
    def create_user_folders_kb(folders: InstrumentedList) -> list:
        folders_kb = []
        row = []
        for folder in folders:
            button = InlineKeyboardButton(text=folder.name, callback_data="fdsaf")
            row.append(button)
            if len(row) == 4:
                folders_kb.append(row.copy())
                row.clear()
        folders_kb.append(row)
        return folders_kb
