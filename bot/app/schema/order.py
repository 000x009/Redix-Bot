import datetime
from enum import Enum
from uuid import UUID
from dataclasses import dataclass, field
from typing import Mapping, Any, Optional, List


class OrderStatus(Enum):
    PAID = 'PAID'
    CLOSED = 'CLOSED'
    COMPLETED = 'COMPLETED'
    PROGRESS = 'PROGRESS'


@dataclass(frozen=True)
class Order:
    id: UUID
    user_id: int
    product_id: UUID
    price: float
    name: str
    additional_data: Mapping[str, Any]
    status: OrderStatus = field(default=OrderStatus.PROGRESS)
    cancel_reason: Optional[str] = field(default=None)
    time: datetime.datetime = field(default=datetime.datetime.now())
    required_fields: Optional[List[str]] = field(default=None)
    admin_id: Optional[int] = field(default=None)
