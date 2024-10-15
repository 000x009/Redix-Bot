from uuid import UUID
from typing import Optional, Union, Any, TypeAlias

from pydantic import BaseModel, EmailStr, Field


class BaseAdditionalData(BaseModel):
    login: Any
    password: Any


class SupercellData(BaseModel):
    email: EmailStr
    code: int = Field(le=999_999, ge=100_000)


class RobloxData(BaseModel):
    login: str
    password: int
    two_factor_code: Optional[int]


class StumbleGuysData(BaseModel):
    nickname: str


class PubgData(BaseModel):
    pubg_id: str


AdditionalData: TypeAlias = Union[
    BaseAdditionalData,
    SupercellData,
    RobloxData,
    StumbleGuysData,
    PubgData,
]


class CreateOrderDTO(BaseModel):
    product_id: UUID
    additional_data: AdditionalData
