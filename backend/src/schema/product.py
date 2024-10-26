from uuid import UUID
from decimal import Decimal
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Product:
    id: UUID
    category_id: int
    name: str
    description: str
    price: Decimal
    game_id: int
    instruction: str = field(default=None)
    purchase_count: int = field(default=0)
    game_name: str = field(default=None)
    category: str = field(default=None)
    image_url: str = field(default=None)
    purchase_limit: int = field(default=None)
    is_manual: bool = field(default=False)
    is_auto_purchase: bool = field(default=False)
    auto_purchase_text: str = field(default=None)
    instruction_image_url: str = field(default=None)
    is_visible: bool = field(default=True)
