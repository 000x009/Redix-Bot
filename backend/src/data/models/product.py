import uuid
from typing import Optional

from sqlalchemy import UUID, String, DECIMAL, Integer, Index, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models import Base


class ProductModel(Base):
    __tablename__ = "product"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey('game.id'), nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL, nullable=False)
    instruction: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    purchase_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    game_name: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String, nullable=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)

    # index = Index(
    #     'product_name_game_category_index',
    #     (
    #         func.coalesce(name, '')
    #         .concat(func.coalesce(game, '')
    #         .concat(func.coalesce(category, ''))).label('columns')
    #     ),
    #     postgresql_using='gin',
    #     postgresql_ops={
    #         'columns': 'gin_trgm_ops',
    #     },
    # )

    orders = relationship('OrderModel', back_populates='product')
    feedbacks = relationship('FeedbackModel', back_populates='product')
    game = relationship('GameModel', back_populates='products')
