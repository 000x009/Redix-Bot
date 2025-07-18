import uuid
from typing import Optional

from sqlalchemy import UUID, String, DECIMAL, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models import Base


class ProductModel(Base):
    __tablename__ = "product"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey('game.id', ondelete='CASCADE'), nullable=True)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('category.id', ondelete='CASCADE'), nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL, nullable=False)
    instruction: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    purchase_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    game_name: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String, nullable=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)
    purchase_limit: Mapped[int] = mapped_column(Integer, nullable=True)
    is_auto_purchase: Mapped[bool] = mapped_column(Boolean, default=False)
    auto_purchase_image_url: Mapped[str] = mapped_column(String, nullable=True)
    auto_purchase_text: Mapped[str] = mapped_column(String, nullable=True)
    is_manual: Mapped[bool] = mapped_column(Boolean, default=False)
    instruction_image_url: Mapped[str] = mapped_column(String, nullable=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    is_gift_purchase: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

    orders = relationship('OrderModel', back_populates='product')
    feedbacks = relationship('FeedbackModel', back_populates='product')
    game = relationship('GameModel', back_populates='products')
    category = relationship('CategoryModel', back_populates='products')
