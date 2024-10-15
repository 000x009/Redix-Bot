import datetime
from enum import StrEnum
from uuid import UUID
from dataclasses import dataclass, field
from typing import Mapping, Any


class OrderStatus(StrEnum):
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
    time: datetime.datetime = field(default=datetime.datetime.now(datetime.UTC))
