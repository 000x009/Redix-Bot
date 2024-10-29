import enum
from typing import List, TYPE_CHECKING

from sqlalchemy.dialects import postgresql
from sqlalchemy import BigInteger, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.models import Base

if TYPE_CHECKING:
    from app.data.models.user import UserModel


class AdminRole(enum.Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"


class AdminModel(Base):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user.user_id"), nullable=False, unique=True)
    role: Mapped[AdminRole] = mapped_column(
        postgresql.ENUM(AdminRole), nullable=False, default=AdminRole.ADMIN
    )
    permissions: Mapped[List[str]] = mapped_column(JSON, nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="admin")
