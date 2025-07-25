from pydantic import BaseModel, Field
from src.services.bilee_service import PaymentMethod
from aiocryptopay.models.invoice import Assets



class TopUpSchema(BaseModel):
    amount: int = Field(ge=10, le=50000)
    method: PaymentMethod = Field(default=PaymentMethod.CARD)


class CryptoPayTopUpSchema(BaseModel):
    amount: int = Field(ge=10, le=50000)
    asset: Assets
