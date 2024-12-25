from typing import TYPE_CHECKING, List

from sqlalchemy import String, ForeignKey, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.models import Base

if TYPE_CHECKING:
    from app.data.models.product import ProductModel


class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey('game.id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    thread_id: Mapped[int] = mapped_column(Integer, nullable=True)
    web_app_place: Mapped[int] = mapped_column(Integer, nullable=True, autoincrement=True)
    required_fields: Mapped[List[str]] = mapped_column(JSON, nullable=True)

    game = relationship('GameModel', back_populates='categories')
    products: Mapped[List["ProductModel"]] = relationship(back_populates="category", uselist=True)
