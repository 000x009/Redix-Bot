from typing import Optional

from sqlalchemy import Integer, DECIMAL, JSON, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models import Base


class UserModel(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    referral_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True, nullable=True)
    balance: Mapped[Optional[float]] = mapped_column(DECIMAL, nullable=True, default=0)
    used_coupons: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    referral_code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String, nullable=True)
    profile_photo: Mapped[str] = mapped_column(String, nullable=True)

    transactions = relationship('TransactionModel', back_populates='user')
    orders = relationship('OrderModel', back_populates='user')
    feedbacks = relationship('FeedbackModel', back_populates='user')
