from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.rates import ExchangeRate
from src.main.config import settings

class CryptopayClientImpl:
    async def create_invoice(
        self,
        amount: float,
        asset: str,
        currency_type: str,
        fiat: str,
        payload: str,
    ) -> str:
        crypto = AioCryptoPay(
            network=Networks.MAIN_NET,
            token=settings.CRYPTO_PAY_API_KEY,
        )
        exchange_rate = await crypto.get_exchange_rates()
        response = await crypto.create_invoice(
            amount=str(round(amount / exchange_rate[0].rate, 2)),
            asset=str(asset),
            currency_type=str(currency_type),
            fiat=str(fiat),
            payload=str(payload),
        )
        await crypto.close()

        return response.mini_app_invoice_url

