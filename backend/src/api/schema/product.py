import uuid
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field


class CreateProduct(BaseModel):
    id: uuid.UUID = Field(default=uuid.uuid4())
    name: str
    description: str
    price: Decimal
    game_id: int
    game_name: Optional[str]
    image_url: Optional[str]
    instruction: Optional[str] = Field(default=None)
    purchase_count: Optional[int] = Field(default=0)
    category: Optional[str] = Field(default=None)
