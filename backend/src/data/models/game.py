from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models import Base

if TYPE_CHECKING:
    from src.data.models.product import ProductModel
    from src.data.models.category import CategoryModel


class GameModel(Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    web_app_place: Mapped[int] = mapped_column(Integer, nullable=True)
    supergroup_id: Mapped[int] = mapped_column(Integer, nullable=True)

    products: Mapped[List["ProductModel"]] = relationship(back_populates="game", uselist=True)
    categories: Mapped[List["CategoryModel"]] = relationship(back_populates="game", uselist=True)
