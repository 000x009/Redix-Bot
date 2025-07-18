import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.data.models import Base


class StarsModel(Base):
    __tablename__ = "stars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rate: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    api_hash: Mapped[str] = mapped_column(String, nullable=False)
    api_cookie: Mapped[str] = mapped_column(String, nullable=False)
    mnemonic: Mapped[str] = mapped_column(String, nullable=False)
