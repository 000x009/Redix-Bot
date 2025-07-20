import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Mapping, Any


class TransactionType(Enum):
    DEBIT = 'Списание'
    DEPOSIT = 'Пополнение'


class TransactionCause(Enum):
    DONATE = 'Донат'
    ADMIN_DEPOSIT = 'Пополнение администратором'
    ADMIN_DEBIT = 'Списание администратором'
    COUPON = 'Ввод промокода'
    REFUND = 'Возврат'
    PAYMENT = 'Оплата заказа'
    REFERRAL = 'Реферальный бонус'


@dataclass(frozen=True)
class Transaction:
    id: int
    unique_id: int
    user_id: int
    type: TransactionType
    cause: TransactionCause
    amount: float
    is_successful: bool = field(default=False)
    time: datetime.datetime = field(default=datetime.datetime.now())
    payment_data: Mapping[str, Any] = field(default=None)
