import uuid
import datetime

from sqlalchemy import UUID, String, ForeignKey, Integer, TIMESTAMP, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models import Base


class FeedbackModel(Base):
    __tablename__ = "feedback"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('product.id'))
    order_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('order.id'))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.user_id', ondelete='CASCADE'))
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    stars: Mapped[int] = mapped_column(Integer, nullable=True)
    time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.now(datetime.UTC))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    user = relationship('UserModel', back_populates='feedbacks')
    product = relationship('ProductModel', back_populates='feedbacks')
    order = relationship('OrderModel', back_populates='feedbacks')
