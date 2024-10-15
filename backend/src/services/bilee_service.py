import random
import hashlib
from time import time
from typing import Mapping, Optional, Any
from enum import Enum

import requests

from src.main.config import settings


class PaymentMethod(Enum):
    CARD = 'card'
    SPB = 'sbp'


class BileeService():
    API_URL = 'https://paymentgate.bilee.ru/api'
    SHOP_ID = settings.BILEE_SHOP_ID
    PASSWORD = settings.BILEE_PASSWORD

    def __init__(self) -> None:
        self.order_id: str = self._generate_order_id()

    def _generate_order_id(self) -> str:
        return str(int(time()) + random.randint(1, 99999))[0:16]
    
    def _generate_signature(self, data: Mapping[str, Optional[str | int]]) -> str:
        data['password'] = self.PASSWORD
        sign = ''.join([str(data.get(key)) for key in sorted(data.keys())])
        return hashlib.sha256(sign.encode('utf-8')).hexdigest()
    
    def _request(self, endpoint: str, data: Mapping[str, Optional[str | int]]) -> Optional[Mapping[str, Optional[str | int]]]:
        headers = {
            'Content-Type': 'application/json'
        }
        data['signature'] = self._generate_signature(data=data)
        response = requests.post(url=f'{self.API_URL}{endpoint}', json=data, headers=headers)

        return response.json()
    
    def create_invoice(
        self,
        amount: int | float,
        method: PaymentMethod = str
    ) -> Optional[Mapping[str, Optional[str | int]]]:
        data = {
            'order_id': self.order_id,
            'method_slug': method,
            'amount': amount,
            'shop_id': self.SHOP_ID,
        }
        return self._request(endpoint='/payment/init', data=data)
    
    def get_invoice(self, order_id: str) -> Optional[Mapping[str, Optional[str | int]]]:
        data = {
            'order_id': order_id,
            'shop_id': self.SHOP_ID,
        }
        return self._request(endpoint='/payment/getOrder', data=data)
    
    def validate_payment(self, __input_signature: str, /, real_payment: Mapping[str, Any]) -> bool:
        real_signature = self._generate_signature(data=real_payment)

        return __input_signature == real_signature 
    