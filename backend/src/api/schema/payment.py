from enum import Enum

from pydantic import BaseModel, Field


class TopUpMethod(Enum):
    SBP = 'sbp'
    CARD = 'card'

class TopUpSchema(BaseModel):
    amount: int = Field(ge=10, le=50000)
    method: TopUpMethod = Field(default=TopUpMethod.CARD)
