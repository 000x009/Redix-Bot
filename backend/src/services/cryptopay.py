from aiocryptopay import AioCryptoPay, Networks
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
        response = await crypto.create_invoice(
            amount=str(amount),
            asset=str(asset),
            currency_type=str(currency_type),
            fiat=str(fiat),
            payload=str(payload),
        )
        await crypto.close()

        return response.mini_app_invoice_url
