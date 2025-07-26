import asyncio
import json
import logging
import random
from typing import Optional, Tuple
from tonutils.client import TonapiClient
from tonutils.wallet import WalletV4R2
import requests
import base64


def get_fragment_headers(cookie: str) -> dict:
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": cookie,
        "Host": "fragment.com",
        "Origin": "https://fragment.com",
        "Referer": "https://fragment.com/stars/buy",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:131.0) Gecko/20010101 Firefox/131.0",
        "X-Requested-With": "XMLHttpRequest"
    }

def get_fragment_url(hash: str) -> str:
    return f"https://fragment.com/api?hash={hash}"


# логи
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stars_purchase.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def decoder(data: str) -> bytes:
    while len(data) % 4 != 0:
        data += "="
    return base64.b64decode(data)

def decoder2(data: bytes) -> str:
    decoded_data = data.decode('latin1')
    ref_id = decoded_data.split("Ref#")[-1]
    return ref_id

def remove_at_symbol(username: str) -> str:
    if username.startswith('@'):
        return username[1:]
    return username

async def check_wallet_balance(mnemonic: list[str]) -> float:
    API_KEY = "AGO5V4UG5EIUDRQAAAAMBAL56YZMLCRO7OKF4D6XT5IHRYI6NL23WD6KLQZWSSVTXLJ6S7I"
    try:
        client = TonapiClient(api_key=API_KEY, is_testnet=False)
        wallet, public_key, private_key, mnemonic = WalletV4R2.from_mnemonic(client, mnemonic)
        balance_nano = await wallet.balance()
        balance_ton = balance_nano 
        logger.info(f"Баланс кошелька: {balance_ton} TON")
        return balance_ton
    except Exception as e:
        logger.error(f"Ошибка при проверке баланса: {e}")
        return 0.0

async def send_ton_transaction(amount: float, comment: str, mnemonic: list[str]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    try:
        client = TonapiClient(api_key="AGO5V4UG5EIUDRQAAAAMBAL56YZMLCRO7OKF4D6XT5IHRYI6NL23WD6KLQZWSSVTXLJ6S7I", is_testnet=False)
        wallet, public_key, private_key, mnemonic = WalletV4R2.from_mnemonic(client, mnemonic)
        
        balance_ton = await check_wallet_balance(mnemonic)
        if balance_ton < amount:
            error_msg = f"Недостаточно средств на кошельке. Требуется: {amount} TON, доступно: {balance_ton} TON."
            logger.warning(error_msg)
            return None, None, error_msg

        tx_hash = await wallet.transfer(
            destination="UQCFJEP4WZ_mpdo0_kMEmsTgvrMHG7K_tWY16pQhKHwoOtFz",
            amount=amount,
            body=comment,
        )
        logger.info(f"Успешно переведено {amount} TON! TX Hash: {tx_hash}")
        
        await asyncio.sleep(random.randint(2, 10))
        
        ref_id = comment.split("Ref#")[-1].strip()
        return tx_hash, ref_id, None
        
    except Exception as e:
        error_msg = f"Ошибка при отправке транзакции: {e}"
        logger.error(error_msg)
        return None, None, error_msg

async def buy_stars(username: str, quantity: int, hash: str, cookie: str, mnemonic: list[str]) -> Tuple[bool, str]:
    min_stars = 50
    max_stars = 1000000
    
    if quantity < min_stars or quantity > max_stars:
        error_msg = f"Недопустимое количество Stars: {quantity}. Разрешено от {min_stars} до {max_stars}."
        logger.error(error_msg)
        return False, error_msg
    
    clean_username = remove_at_symbol(username)
    logger.info(f"Покупаем {quantity} Stars для пользователя: {clean_username}")
    
    url = get_fragment_url(hash)
    headers = get_fragment_headers(cookie)
    
    # получаем recipient из username
    payload_search = {
        "query": clean_username,
        "quantity": quantity,
        "method": "searchStarsRecipient"
    }
    
    try:
        print(hash, flush=True)
        print(cookie, flush=True)
        print(mnemonic, flush=True)

        print("\n\n", flush=True)
        print(payload_search, flush=True)
        print(url, flush=True)
        print(headers, flush=True)
        response_search = requests.post(url, headers=headers, data=payload_search)
        response_search.raise_for_status()
        
        if not response_search.text:
            error_msg = "Пустой ответ от сервера Fragment при поиске recipient."
            logger.error(error_msg)
            return False, error_msg
        
        text_search = response_search.json()
        logger.info(f"Ответ поиска recipient: {text_search}")
        
    except requests.RequestException as e:
        error_msg = f"Ошибка при запросе поиска recipient: {e}"
        logger.error(error_msg)
        return False, error_msg
    except json.JSONDecodeError as e:
        error_msg = f"Не удалось декодировать JSON: {e}. Ответ сервера: {response_search.text}"
        logger.error(error_msg)
        return False, error_msg
    
    if text_search.get('ok') is True:
        recipient = text_search.get('found', {}).get('recipient')
        if not recipient:
            error_msg = f"Recipient не найден в ответе: {text_search}"
            logger.error(error_msg)
            return False, error_msg
    else:
        error_detail = text_search.get('error', 'Неизвестная ошибка при поиске recipient.')
        error_msg = f"Ошибка при поиске recipient: {error_detail}"
        logger.error(error_msg)
        return False, error_msg
    
    # покупка
    payload_init = {
        "recipient": recipient,
        "quantity": quantity,
        "method": "initBuyStarsRequest"
    }
    
    try:
        response_init = requests.post(url, headers=headers, data=payload_init)
        response_init.raise_for_status()
        
        if not response_init.text:
            error_msg = "Пустой ответ от сервера Fragment при инициализации покупки."
            logger.error(error_msg)
            return False, error_msg
        
        text_init = response_init.json()
        logger.info(f"Ответ инициализации покупки: {text_init}")
        
    except requests.RequestException as e:
        error_msg = f"Ошибка при инициализации покупки Stars: {e}"
        logger.error(error_msg)
        return False, error_msg
    except json.JSONDecodeError as e:
        error_msg = f"Не удалось декодировать JSON: {e}. Ответ сервера: {response_init.text}"
        logger.error(error_msg)
        return False, error_msg
    
    req_id = text_init.get('req_id')
    try:
        AMOUNT = float(text_init.get('amount', 0))
        logger.info(f"Требуемая сумма: {AMOUNT} TON")
    except (TypeError, ValueError):
        AMOUNT = 0
        logger.error("Не удалось конвертировать 'amount' в float.")
    
    if not req_id or AMOUNT == 0:
        error_msg = f"Не удалось получить req_id или amount: {text_init}"
        logger.error(error_msg)
        return False, error_msg
    
    payload_link = {
        "account": '{"address":"0:adc5b49f73e4796ecc3c290ad0d89f87fa552b515d173d5295469df9612c24a","chain":"-239","walletStateInit":"te6ccgECFgEAAwQAAgE0AQIBFP8A9KQT9LzyyAsDAFEAAAAAKamjF5hE%2BFriD8Ufe710n9USsAZBzBxLOlXNYCYDiPBRvJZXQAIBIAQFAgFIBgcE%2BPKDCNcYINMf0x%2FT%2F%2FQE0VFDuvKhUVG68qIF%2BQFUEGT5EPKj%2BAAkpMjLH1JAyx9SMMv%2FUhD0AMntVPgPAdMHIcAAn2xRkyDXSpbTB9QC%2BwDoMOAhwAHjACHAAuMAAcADkTDjDQOkyMsfEssfy%2F8SExQVAubQAdDTAyFxsJJfBOAi10nBIJJfBOAC0x8hghBwbHVnvSKCEGRzdHK9sJJfBeAD%2BkAwIPpEAcjKB8v%2FydDtRNCBAUDXIfQEMFyBAQj0Cm%2BhMbOSXwfgBdM%2FyCWCEHBsdWe6kjgw4w0DghBkc3RyupJfBuMNCAkCASAKCwB4AfoA9AQw%2BCdvIjBQCqEhvvLgUIIQcGx1Z4MesXCAGFAEywUmzxZY%2BgIZ9ADLaRfLH1Jgyz8gyYBA%2BwAGAIpQBIEBCPRZMO1E0IEBQNcgyAHPFvQAye1UAXKwjiOCEGRzdHKDHrFwgBhQBcsFUAPPFiP6AhPLassfyz%2FJgED7AJJfA%2BICASAMDQBZvSQrb2omhAgKBrkPoCGEcNQICEekk30pkQzmkD6f%2BYN4EoAbeBAUiYcVnzGEAgFYDg8AEbjJftRNDXCx%2BAA9sp37UTQgQFA1yH0BDACyMoHy%2F%2FJ0AGBAQj0Cm%2BhMYAIBIBARABmtznaiaEAga5Drhf%2FAABmvHfaiaEAQa5DrhY%2FAAG7SB%2FoA1NQi%2BQAFyMoHFcv%2FydB3dIAYyMsFywIizxZQBfoCFMtrEszMyXP7AMhAFIEBCPRR8qcCAHCBAQjXGPoA0z%2FIVCBHgQEI9FHyp4IQbm90ZXB0gBjIywXLAlAGzxZQBPoCE8tqEszMyXP7AMhAFIEBCPRR8qcCAHCBAQjXGPoA0z%2FIVCBHgQEI9FHyp4IQZHN0cnB0gBjIywXLAlAFzxZQA%2FoCE8tqyx8Syz%2FJc%2FsAAAr0AMntVA%3D%3D"}',
        "device": '{"platform":"android","appName":"Tonkeeper","appVersion":"5.0.18","maxProtocolVersion":2,"features":["SendTransaction",{"name":"SendTransaction","maxMessages":4}]}',
        "transaction": "1",
        "id": req_id,
        "show_sender": "0",
        "method": "getBuyStarsLink"
    }
    
    try:
        response_link = requests.post(url, headers=headers, data=payload_link)
        response_link.raise_for_status()
        
        if not response_link.text:
            error_msg = "Пустой ответ от сервера Fragment при получении ссылки на покупку."
            logger.error(error_msg)
            return False, error_msg
        
        text_link = response_link.json()
        logger.info(f"Ответ получения ссылки на покупку: {text_link}")
        
    except requests.RequestException as e:
        error_msg = f"Ошибка при получении ссылки на покупку Stars: {e}"
        logger.error(error_msg)
        return False, error_msg
    except json.JSONDecodeError as e:
        error_msg = f"Не удалось декодировать JSON: {e}. Ответ сервера: {response_link.text}"
        logger.error(error_msg)
        return False, error_msg
    
    if text_link.get('ok') is True:
        transaction_messages = text_link.get('transaction', {}).get('messages', [])
        logger.info(f"Сообщения транзакции: {transaction_messages}")
        
        if not transaction_messages:
            error_msg = f"Сообщения транзакции не найдены: {text_link}"
            logger.error(error_msg)
            return False, error_msg
        
        payload_transaction = transaction_messages[0].get('payload')
        logger.info(f"Payload транзакции: {payload_transaction}")
        
        if not payload_transaction:
            error_msg = f"Payload сообщения транзакции не найден: {text_link}"
            logger.error(error_msg)
            return False, error_msg
        
        try:
            decoded_payload = decoder(payload_transaction)
            ref_id = decoder2(data=decoded_payload)
            COMMENT = f"{quantity} Telegram Stars \n\nRef#{ref_id}"
            logger.info(f"Комментарий для транзакции: {COMMENT}")
        except Exception as e:
            error_msg = f"Ошибка при обработке payload транзакции: {e}"
            logger.error(error_msg)
            return False, error_msg
    else:
        error_detail = text_link.get('error', 'Неизвестная ошибка при получении ссылки на покупку Stars.')
        error_msg = f"Ошибка при получении ссылки на покупку Stars: {error_detail}"
        logger.error(error_msg)
        return False, error_msg
    
    try:
        tx_hash, ref_id, error_transaction = await send_ton_transaction(AMOUNT, COMMENT, mnemonic)
        if error_transaction:
            return False, error_transaction
        if not tx_hash or not ref_id:
            error_msg = "Не удалось получить данные транзакции после отправки."
            logger.error(error_msg)
            return False, error_msg
    except Exception as e:
        error_msg = f"Исключение при отправке транзакции: {e}"
        logger.error(error_msg)
        return False, error_msg
    
    success_msg = f"✅ Успешно куплено {quantity} Stars для {clean_username}!\n"
    success_msg += f"🔗 Транзакция: https://tonviewer.com/transaction/{tx_hash}\n"
    success_msg += f"🔑 Ref ID: {ref_id}"
    logger.info(success_msg)
    return True, success_msg
