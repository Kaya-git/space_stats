from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base
import sqlalchemy as sa
from datetime import datetime
import uuid
import enum
from typing import List


UUID_ID = uuid.UUID


class Role(enum.StrEnum):
    Client = "Клиент"
    Admin = "Администратор"


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    registered_on: Mapped[int] = mapped_column(
        sa.TIMESTAMP,
        default=datetime.utcnow,
        nullable=False
    )

    api_keys: Mapped[List["ApiKey"]] = relationship(
        back_populates="user",
        cascade="all,delete"
    )

    def __str__(self) -> str:
        return f"{self.email}"

    def __repr__(self) -> str:
        return f"{self.email}"


class ApiKey(Base):
    __tablename__ = 'api_key'

    id: Mapped[UUID_ID] = mapped_column(
        sa.Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    key_name: Mapped[str] = mapped_column(
        sa.String(length=55)
    )
    hashed_key: Mapped[str] = mapped_column(
        sa.String(length=1024),
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.id", ondelete="Cascade"),
        nullable=True
    )

    user: Mapped["User"] = relationship(
        back_populates="api_keys"
    )
