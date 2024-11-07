from enum import Enum

from pydantic import BaseModel, Field
from src.services.freekassa_service import PaymentMethod


class TopUpSchema(BaseModel):
    amount: int = Field(ge=10, le=50000)
    method: PaymentMethod = Field(default=PaymentMethod.CARD)
