import enum
import uuid
import datetime
from typing import Mapping, Any

from sqlalchemy import DECIMAL, Enum, UUID, TIMESTAMP, BigInteger, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models import Base
from src.schema.transaction import TransactionType, TransactionCause


class TransactionModel(Base):
    __tablename__ = "transaction"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.user_id', ondelete='CASCADE'))
    type: Mapped[enum.Enum] = mapped_column(Enum(TransactionType), nullable=False)
    cause: Mapped[str] = mapped_column(Enum(TransactionCause), nullable=False)
    time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.now(datetime.UTC))
    amount: Mapped[float] = mapped_column(DECIMAL)
    payment_data: Mapped[Mapping[str, Any]] = mapped_column(JSON, nullable=True)
    is_successful: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    user = relationship('UserModel', back_populates='transactions')
    