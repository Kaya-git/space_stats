from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base
import sqlalchemy as sa
from datetime import datetime
import uuid
import enum


UUID_ID = uuid.UUID


class Role(enum.StrEnum):
    Client = "Клиент"
    Admin = "Администратор"


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        sa.String(length=320),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        sa.String(length=1024),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=True,
        nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=False,
        nullable=False,
    )
    registered_on: Mapped[int] = mapped_column(
        sa.TIMESTAMP,
        default=datetime.utcnow,
        nullable=False
    )

    hashed_api_keys: Mapped[int] = relationship(
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
        back_populates="hashed_api_keys"
    )
