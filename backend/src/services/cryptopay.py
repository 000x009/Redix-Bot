from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.invoice import Assets
from src.main.config import settings

class CryptopayClientImpl:
    async def create_invoice(
        self,
        amount: float,
        asset: str,
        currency_type: str,
        payload: str,
    ) -> str:
        crypto = AioCryptoPay(
            network=Networks.MAIN_NET,
            token=settings.CRYPTO_PAY_API_KEY,
        )
        exchange_rate = await crypto.get_exchange_rates()
        response = await crypto.create_invoice(
            amount=round(amount / exchange_rate[0].rate, 2),
            currency_type=str(currency_type),
            payload=str(payload),
            accepted_assets=[
                Assets.BTC,
                Assets.USDT,
                Assets.TON,
                Assets.ETH,
                Assets.USDC,
                Assets.BNB,
                Assets.TRX,
                Assets.LTC,
                Assets.GRAM,
                Assets.NOT,
                Assets.MY,
                Assets.SOL,
                Assets.DOGS,
                Assets.HMSTR,
                Assets.CATI,
                Assets.DOGE,
            ],
            swap_to="USDT",
        )
        await crypto.close()

        return response.mini_app_invoice_url

