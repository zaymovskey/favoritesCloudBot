from sqlalchemy import insert, select

from database import session
from models import User


class UserService:

    def __init__(self):
        self.session = session

    def add_user_if_not_exists(self, user_id: int) -> None:
        stmt = select(User).where(
            User.user_id == user_id
        )
        user = self.session.execute(stmt).fetchall()

        if not user:
            insert_statement = insert(User).values(user_id=user_id)
            self.session.execute(insert_statement)
            self.session.commit()
