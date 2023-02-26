from datetime import datetime
from typing import List

from database import Base

from sqlalchemy import (
    Integer,
    func,
    DateTime,
    Enum,
    String,
    ForeignKey,
    BigInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
    backref,
)


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    current_menu: Mapped[List[str]] = mapped_column(
        "current_menu",
        Enum("add_folder", name="menu_enum", create_type=False),
        nullable=True,
    )

    current_folder_id: Mapped[int] = mapped_column(Integer, nullable=True)

    folders: Mapped[List["Folder"]] = relationship(back_populates="user")
    files: Mapped[List["File"]] = relationship(back_populates="user")

    time_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Folder(Base):
    __tablename__ = "folder"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    user: Mapped["User"] = relationship(back_populates="folders")

    files: Mapped[List["File"]] = relationship(back_populates="folder")

    time_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    parent_id = mapped_column(Integer, ForeignKey("folder.id"))
    children = relationship("Folder", backref=backref("parent", remote_side=[id]))

    __table_args__ = (
        UniqueConstraint("user_id", "parent_id", "name", name="folders_unique"),
    )


class File(Base):
    __tablename__ = "file"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_id: Mapped[int] = mapped_column(BigInteger)
    filename: Mapped[str] = mapped_column(String(255))
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

    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    user: Mapped["User"] = relationship(back_populates="files")

    folder_id: Mapped[int] = mapped_column(ForeignKey("folder.id"))
    folder: Mapped["Folder"] = relationship(back_populates="files")

    time_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
