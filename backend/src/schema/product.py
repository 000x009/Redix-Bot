from uuid import UUID
from decimal import Decimal
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Product:
    id: UUID
    name: str
    description: str
    price: Decimal
    game_id: int
    instruction: str = field(default=None)
    purchase_count: int = field(default=0)
    game_name: str = field(default=None)
    category: str = field(default=None)
    image_url: str = field(default=None)
