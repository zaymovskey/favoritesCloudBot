from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    func,
    DateTime,
    Enum,
)
import os
from sqlalchemy.orm import declarative_base

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    current_menu = Column(
        "current_menu", Enum("add_folder", name="menu_enum", create_type=False)
    )
    time_created = Column(DateTime(timezone=True), server_default=func.now())
