from typing import Optional, TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Integer, DECIMAL, JSON, String, BigInteger, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models import Base

if TYPE_CHECKING:
    from src.data.models.admin import AdminModel


class UserModel(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    referral_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True, nullable=True)
    balance: Mapped[Optional[float]] = mapped_column(DECIMAL, nullable=True, default=0)
    used_coupons: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    referral_code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String, nullable=True)
    profile_photo: Mapped[str] = mapped_column(String, nullable=True)
    joined_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=datetime.now(), server_default=func.now())

    transactions = relationship('TransactionModel', back_populates='user')
    orders = relationship('OrderModel', back_populates='user')
    feedbacks = relationship('FeedbackModel', back_populates='user')
    admin: Mapped["AdminModel"] = relationship(back_populates="user")
