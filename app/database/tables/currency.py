from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.tables.base import Base


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str | None] = mapped_column(String(255))
    code: Mapped[str | None] = mapped_column(String(255))
    rate: Mapped[float | None] = mapped_column(Numeric(precision=100, scale=20))


class CurrencyLastUpdate(Base):
    __tablename__ = "last_currency_update"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_update: Mapped[DateTime] = mapped_column(DateTime())
