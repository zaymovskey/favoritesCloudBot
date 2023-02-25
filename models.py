from datetime import datetime
from typing import List

from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Integer,
    func,
    DateTime,
    Enum,
    String,
    ForeignKey,
)
import os
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    current_menu: Mapped[List[str]] = mapped_column(
        "current_menu", Enum("add_folder", name="menu_enum", create_type=False)
    )
    folders: Mapped[List["Folder"]] = relationship(back_populates="user")
    files: Mapped[List["File"]] = relationship(back_populates="user")

    time_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Folder(Base):
    __tablename__ = "folder"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="folders")
    files: Mapped[List["File"]] = relationship(back_populates="folder")

    time_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class File(Base):
    __tablename__ = "file"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[List[str]] = mapped_column(
        "file_type",
        Enum(
            "photo",
            "document",
            "video",
            "audio",
            name="file_types_enum",
            create_type=False,
        ),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="folders")
    folder_id: Mapped[int] = mapped_column(ForeignKey("folder.id"))
    folder: Mapped["Folder"] = relationship(back_populates="files")

    time_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
