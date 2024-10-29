import uuid
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Any

from pydantic import BaseModel, field_validator


class PromoStatus(Enum):
    ACTIVE = 'Активен'
    INACTIVE = 'Неактивен'


@dataclass(frozen=True)
class Promo():
    name: str
    bonus_amount: float
    uses: int
    id: uuid.UUID = field(default=uuid.uuid4())
    status: PromoStatus = field(default=PromoStatus.ACTIVE)


class RawPromo(BaseModel):
    name: str
