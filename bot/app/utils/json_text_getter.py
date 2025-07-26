import json
import os
import uuid
from typing import Optional

from app.schema import Product

from uuid import UUID

from pydantic import BaseModel


class CreateOrderDTO(BaseModel):
    product_id: UUID
    additional_data: dict



def get_json_text(key: str) -> Optional[str]:
    with open(os.path.normpath('app/files/texts.json'), encoding="utf-8") as f:
        data = json.load(f)

        return data.get(key)
    

def get_order_info_text(
    user_id: int,
    order_id: uuid.UUID,
    order_data: CreateOrderDTO,
    product: Product,
    category: str,
    username: str | None = None,
    fullname: str | None = None,
) -> str:
    game_name = product.game_name.strip()
    if game_name == 'Clash Royale':
        game_name = 'Clash of Clans'
    elif game_name == 'Clash of Clans':
        game_name = 'Clash Royale'

    username = username if username else fullname
    order_text = get_json_text('order_text').format(
        order_id=order_id,
        username=username,
        user_id=user_id,
        game=game_name,
        category=category,
        product_name=product.name,
        product_price=product.price
    )

    additional_data_text = ""
    for key, value in order_data.items():
        additional_data_text += f"\n<b>{key}</b>: <code>{value}</code>"

    return order_text + additional_data_text


def get_order_info_text_stars(
    user_id: int,
    order_id: uuid.UUID,
    order_data: CreateOrderDTO,
    product: Product,
    category: str,
    username: str | None = None,
    fullname: str | None = None,
) -> str:
    game_name = product.game_name.strip()
    if game_name == 'Clash Royale':
        game_name = 'Clash of Clans'
    elif game_name == 'Clash of Clans':
        game_name = 'Clash Royale'

    username = username if username else fullname
    order_text = get_json_text('order_text_stars').format(
        order_id=order_id,
        username=username,
        user_id=user_id,
        game=game_name,
        category=category,
        product_name=product.name,
        product_price=product.price
    )

    additional_data_text = ""
    for key, value in order_data.items():
        additional_data_text += f"\n<b>{key}</b>: <code>{value}</code>"

    return order_text + additional_data_text