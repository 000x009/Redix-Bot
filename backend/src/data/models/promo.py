import uuid
import enum

from sqlalchemy import DECIMAL, String, Integer, Enum, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models import Base
from src.schema.promo import PromoStatus


class PromoModel(Base):
    __tablename__ = "promo"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4())
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    bonus_amount: Mapped[float] = mapped_column(DECIMAL)
    uses: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[enum.Enum] = mapped_column(Enum(PromoStatus), default=PromoStatus.ACTIVE)
