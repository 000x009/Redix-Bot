import datetime
from uuid import UUID
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Feedback:
    id: UUID
    product_id: UUID
    order_id: UUID
    user_id: int
    text: str
    stars: int = field(default=None)
    time: datetime.datetime = field(default=datetime.datetime.now())
    is_active: bool = field(default=True)
    images: list[str] = field(default=None)
