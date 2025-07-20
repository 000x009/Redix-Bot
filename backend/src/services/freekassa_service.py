import requests
import enum
import hashlib
import hmac
from typing import Optional, Dict

from src.main.config import settings

class PaymentMethod(enum.Enum):
    CARD = 36
    SBP = 44


class FreeKassaService:
    API_URL = 'https://api.freekassa.com/v1/'

    def __init__(self) -> None:
        self.shop_id = None
        self.secret_key = None

    def create_order(
        self,
        amount: float,
        ip: str,
        email: str,
        payment_method: PaymentMethod,
        unique_transaction_id: int,
    ) -> Optional[Dict]:
        endpoint = '/orders/create'
        print(unique_transaction_id, flush=True)
        params = {
            'shopId': self.shop_id,
            'amount': amount,
            'currency': 'RUB',
            'ip': ip,
            'nonce': unique_transaction_id,
            'email': email,
            'i': payment_method.value,
        }
        params['signature'] = self._generate_signature(params)

        response = requests.post(f'{self.API_URL}{endpoint}', json=params)
        print(response.json(), flush=True)
        return response.json()

    def _generate_signature(self, params: Dict[str, str]) -> str:
        sorted_params = {key: params[key] for key in sorted(params.keys())}
        sign_string = '|'.join([str(value) for value in sorted_params.values()])
        signature = hmac.new(self.secret_key.encode('utf-8'), sign_string.encode('utf-8'), hashlib.sha256).hexdigest()

        return signature
