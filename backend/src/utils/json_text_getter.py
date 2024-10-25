import json
import os
import uuid
from typing import Optional

from src.api.schema.order import (
    CreateOrderDTO,
    SupercellData,
    RobloxData,
    BaseAdditionalData,
    PubgData,
    StumbleGuysData,
)
from src.schema import Product, Category


def get_json_text(key: str) -> Optional[str]:
    with open(os.path.normpath('src/files/texts.json'), encoding="utf-8") as f:
        data = json.load(f)

        return data.get(key)
    

def get_order_info_text(
    user_id: int,
    order_id: uuid.UUID,
    order_data: CreateOrderDTO | dict,
    product: Product,
    category: str,
) -> Optional[str]:
    if product.game_name in ('Clash of Clans', 'Clash Royale', 'Brawl Stars', 'Squad Busters'):
        return get_json_text('supercell_order').format(
            order_id=order_id,
            user_id=user_id,
            game=product.game_name,
            product_name=product.name,
            product_price=product.price,
            email=order_data.additional_data.email if not isinstance(order_data, dict) else order_data.get('email'),
            code=order_data.additional_data.code if not isinstance(order_data, dict) else order_data.get('code'),
            category=category,
        )
    elif product.game_name == 'Roblox':
        return get_json_text('roblox_order').format(
            order_id=order_id,
            user_id=user_id,
            game=product.game_name,
            product_name=product.name,
            product_price=product.price,
            email=order_data.additional_data.login,
            password=order_data.additional_data.password if not isinstance(order_data, dict) else order_data.get('password'),
            two_factor_code=order_data.additional_data.two_factor_code if not isinstance(order_data, dict) else order_data.get('two_factor_code'),
            category=category,
        )
    elif product.game_name == 'PUBG':
        return get_json_text('pubg_order').format(
            order_id=order_id,
            user_id=user_id,
            game=product.game_name,
            product_name=product.name,
            product_price=product.price,
            pubg_id=order_data.additional_data.pubg_id if not isinstance(order_data, dict) else order_data.get('pubg_id'),
            category=category,
        )
    elif product.game_name == 'Stumble Guys':
        return get_json_text('stumble_guys_order').format(
            order_id=order_id,
            user_id=user_id,
            game=product.game_name,
            product_name=product.name,
            product_price=product.price,
            nickname=order_data.additional_data.nickname if not isinstance(order_data, dict) else order_data.get('nickname'),
            category=category,
        )
    else:
        return get_json_text('base_order').format(
            order_id=order_id,
            user_id=user_id,
            game=product.game_name,
            product_name=product.name,
            product_price=product.price,
            login=order_data.additional_data.login if not isinstance(order_data, dict) else order_data.get('login'),
            password=order_data.additional_data.password if not isinstance(order_data, dict) else order_data.get('password'),
            category=category,
        )