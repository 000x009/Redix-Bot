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
    print("gameName Bot", product.game_name, flush=True)
    game_name = product.game_name.strip()
    print(game_name == 'Clash Royale')
    if game_name == 'Clash Royale':
        game_name = 'Clash of Clans'
    if game_name == 'Clash of Clans':
        game_name = 'Clash Royale'

    print("GAME NAME NEW", game_name)

    order_text = get_json_text('order_text').format(
        order_id=order_id,
        user_id=user_id,
        game=game_name,
        category=category,
        product_name=product.name,
        product_price=product.price
    )

    # if product.game_name == 'Clash of Clans':
    #     order_text.replace('Clash of Clans', 'Clash Royale')
    # if product.game_name == 'Clash Royale':
    #     order_text.replace('Clash Royale', 'Clash of Clans')
    
    print(order_text)

    additional_data_text = ""
    for key, value in order_data.items():
        additional_data_text += f"\n<b>{key}</b>: <code>{value}</code>"

    return order_text + additional_data_text