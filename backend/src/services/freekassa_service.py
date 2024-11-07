import requests
import enum
import hashlib
import hmac
import time
from typing import Optional, Dict

from src.main.config import settings

class PaymentMethod(enum.Enum):
    CARD = 36
    SBP = 44


class FreeKassaService:
    API_URL = 'https://api.freekassa.com/v1/'

    def __init__(self) -> None:
        self.shop_id = settings.FREEKASSA_SHOP_ID
        self.secret_key = settings.FREEKASSA_SECRET_KEY

    def create_order(
        self,
        amount: float,
        ip: str,
        email: str,
        payment_method: PaymentMethod,
    ) -> Optional[Dict]:
        endpoint = '/orders/create'
        params = {
            'shopId': self.shop_id,
            'amount': amount,
            'currency': 'RUB',
            'ip': ip,
            'nonce': self._generate_nonce(),
            'email': email,
            'i': payment_method.value,
        }
        params['signature'] = self._generate_signature(params)

        response = requests.post(f'{self.API_URL}{endpoint}', json=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def _generate_signature(self, params: Dict[str, str]) -> str:
        sorted_params = {key: params[key] for key in sorted(params.keys())}
        sign_string = '|'.join([str(value) for value in sorted_params.values()])
        signature = hmac.new(self.secret_key.encode('utf-8'), sign_string.encode('utf-8'), hashlib.sha256).hexdigest()

        return signature

    def _generate_nonce(self) -> int:
        current_time = time.time()
        random_number = int((current_time - int(current_time)) * 1000000)
        return random_number
