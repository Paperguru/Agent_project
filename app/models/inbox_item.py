from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class InboxItemModel(Base):
    __tablename__= "inbox_items"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    Priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    require_action: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default= False,
    )

    due_date: Mapped[str] = mapped_column(
        Date,
        nullable=False,
    )

    people: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]"
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="new"
    )

    created_at: Mapped[str] = mapped_column(
        DateTime,
        nullable=False,
    )