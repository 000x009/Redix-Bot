from typing import TYPE_CHECKING, List

from sqlalchemy import String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models import Base

if TYPE_CHECKING:
    from src.data.models.product import ProductModel


class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey('game.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    thread_id: Mapped[int] = mapped_column(Integer, nullable=True)
    web_app_place: Mapped[int] = mapped_column(Integer, nullable=True, autoincrement=True)

    game = relationship('GameModel', back_populates='categories')
    products: Mapped[List["ProductModel"]] = relationship(back_populates="category", uselist=True)
