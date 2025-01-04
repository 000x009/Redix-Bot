import json
import os
import uuid
from typing import Optional

from src.api.schema.order import CreateOrderDTO
from src.schema import Product


def get_json_text(key: str) -> Optional[str]:
    with open(os.path.normpath('src/files/texts.json'), encoding="utf-8") as f:
        data = json.load(f)

        return data.get(key)
    

def get_order_info_text(
    user_id: int,
    order_id: uuid.UUID,
    order_data: CreateOrderDTO,
    product: Product,
    category: str,
) -> Optional[str]:
    if product.game_name == 'Clash Royale':
        product.game_name == 'Clash of Clans'
    elif product.game_name == 'Clash of Clans':
        product.game_name == 'Clash Royale'

    order_text = get_json_text('order_text').format(
        order_id=order_id,
        user_id=user_id,
        game=product.game_name,
        category=category,
        product_name=product.name,
        product_price=product.price
    )

    additional_data_text = ""
    for key, value in order_data.items():
        additional_data_text += f"\n<b>{key}</b>: <code>{value}</code>"

    return order_text + additional_data_text