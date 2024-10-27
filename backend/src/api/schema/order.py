from uuid import UUID

from pydantic import BaseModel


class CreateOrderDTO(BaseModel):
    product_id: UUID
    additional_data: dict
