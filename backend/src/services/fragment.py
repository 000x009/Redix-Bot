import json
import os
import sys
import asyncio
import logging
import random
import base64
import requests
from typing import Optional, Tuple
from tonutils.client import TonapiClient
from tonutils.wallet import WalletV4R2

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stars_purchase.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FragmentAPI:
    DEFAULT_CONFIG = {
        "API_KEY": "AGO5V4UG5EIUDRQAAAAMBAL56YZMLCRO7OKF4D6XT5IHRYI6NL23WD6KLQZWSSVTXLJ6S7I",
        "IS_TESTNET": False,
        "MNEMONIC": None,
        "DESTINATION_ADDRESS": "UQCFJEP4WZ_mpdo0_kMEmsTgvrMHG7K_tWY16pQhKHwoOtFz",
        "MIN_STARS": 50,
        "MAX_STARS": 1000000,
        "fragment_api": {
            "hash": "YOUR_FRAGMENT_HASH",
            "cookie": "YOUR_FRAGMENT_COOKIE",
            "url": "https://fragment.com/api"
        },
        "SHOW_SENDER": "0"  # 0 - не показывать, 1 - показывать 
    }

    def __init__(self, config: Optional[dict] = None):
        """Initialize FragmentAPI with optional configuration."""
        self.config = self._load_config(config)
        self.headers = self._get_fragment_headers()
        self.api_url = self._get_fragment_url()

    def _load_config(self, config: Optional[dict] = None) -> dict:
        """Load and validate configuration."""
        if config is None:
            if os.path.exists("stars_config.json"):
                with open("stars_config.json", 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}

        # Merge with default config
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)

        # Ensure fragment_api section exists
        if "fragment_api" not in final_config:
            final_config["fragment_api"] = self.DEFAULT_CONFIG["fragment_api"]
        else:
            for key in self.DEFAULT_CONFIG["fragment_api"]:
                if key not in final_config["fragment_api"]:
                    final_config["fragment_api"][key] = self.DEFAULT_CONFIG["fragment_api"][key]

        return final_config

    def _get_fragment_headers(self) -> dict:
        """Get headers for Fragment API requests."""
        return {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": self.config["fragment_api"]["cookie"],
            "Host": "fragment.com",
            "Origin": "https://fragment.com",
            "Referer": "https://fragment.com/stars/buy",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:131.0) Gecko/20010101 Firefox/131.0",
            "X-Requested-With": "XMLHttpRequest"
        }

    def _get_fragment_url(self) -> str:
        """Get Fragment API URL with hash."""
        return f"{self.config['fragment_api']['url']}?hash={self.config['fragment_api']['hash']}"

    @staticmethod
    def _decode_payload(data: str) -> bytes:
        """Decode base64 payload."""
        while len(data) % 4 != 0:
            data += "="
        return base64.b64decode(data)

    @staticmethod
    def _extract_ref_id(data: bytes) -> str:
        """Extract reference ID from decoded payload."""
        decoded_data = data.decode('latin1')
        return decoded_data.split("Ref#")[-1]

    @staticmethod
    def _remove_at_symbol(username: str) -> str:
        """Remove @ symbol from username if present."""
        return username[1:] if username.startswith('@') else username

    async def check_wallet_balance(self) -> float:
        """Check TON wallet balance."""
        try:
            client = TonapiClient(api_key=self.config["API_KEY"], is_testnet=self.config["IS_TESTNET"])
            wallet, _, _, _ = WalletV4R2.from_mnemonic(client, self.config["MNEMONIC"])
            balance_ton = await wallet.balance()
            logger.info(f"Баланс кошелька: {balance_ton} TON")
            return balance_ton
        except Exception as e:
            logger.error(f"Ошибка при проверке баланса: {e}")
            return 0.0

    async def send_ton_transaction(self, amount: float, comment: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Send TON transaction."""
        try:
            client = TonapiClient(api_key=self.config["API_KEY"], is_testnet=self.config["IS_TESTNET"])
            wallet, _, _, _ = WalletV4R2.from_mnemonic(client, self.config["MNEMONIC"])
            
            balance_ton = await self.check_wallet_balance()
            if balance_ton < amount:
                error_msg = f"Недостаточно средств на кошельке. Требуется: {amount} TON, доступно: {balance_ton} TON."
                logger.warning(error_msg)
                return None, None, error_msg

            tx_hash = await wallet.transfer(
                destination=self.config["DESTINATION_ADDRESS"],
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
    
    def set_hash_and_cookie(self, hash: str, cookie: str, mnemonic: list[str]) -> None:
        self.config["fragment_api"]["hash"] = hash
        self.config["fragment_api"]["cookie"] = cookie
        self.config["MNEMONIC"] = mnemonic

    async def buy_stars(self, username: str, quantity: int, cookie: str, hash: str, mnemonic: list[str]) -> Tuple[bool, str]:
        """Buy Telegram Stars for a user."""
        min_stars = self.config.get("MIN_STARS", 50)
        max_stars = self.config.get("MAX_STARS", 1000000)
        print(hash, flush=True)
        print(cookie, flush=True)
        print(mnemonic, flush=True)
        
        if quantity < min_stars or quantity > max_stars:
            error_msg = f"Недопустимое количество Stars: {quantity}. Разрешено от {min_stars} до {max_stars}."
            logger.error(error_msg)
            return False, error_msg
        
        clean_username = self._remove_at_symbol(username)
        logger.info(f"Покупаем {quantity} Stars для пользователя: {clean_username}")
        
        # Get recipient
        self.set_hash_and_cookie(hash, cookie, mnemonic)
        payload_search = {
            "query": clean_username,
            "quantity": quantity,
            "method": "searchStarsRecipient"
        }
        
        try:
            print(self.config, flush=True)
            print(payload_search, flush=True)
            print(self.api_url, flush=True)
            print(self.headers, flush=True)
            api_url = f"{self.config['fragment_api']['url']}?hash={self.config['fragment_api']['hash']}"
            response_search = requests.post(api_url, headers=self.headers, data=payload_search)
            response_search.raise_for_status()
            
            if not response_search.text:
                error_msg = "Пустой ответ от сервера Fragment при поиске recipient."
                logger.error(error_msg)
                return False, error_msg
            
            text_search = response_search.json()
            logger.info(f"Ответ поиска recipient: {text_search}")
            
        except (requests.RequestException, json.JSONDecodeError) as e:
            error_msg = f"Ошибка при поиске recipient: {e}"
            logger.error(error_msg)
            return False, error_msg
        
        if not text_search.get('ok'):
            error_msg = f"Ошибка при поиске recipient: {text_search.get('error', 'Unknown error')}"
            logger.error(error_msg)
            return False, error_msg

        recipient = text_search.get('found', {}).get('recipient')
        if not recipient:
            error_msg = f"Recipient не найден в ответе: {text_search}"
            logger.error(error_msg)
            return False, error_msg
        
        # Initialize purchase
        payload_init = {
            "recipient": recipient,
            "quantity": quantity,
            "method": "initBuyStarsRequest"
        }
        
        try:
            response_init = requests.post(api_url, headers=self.headers, data=payload_init)
            response_init.raise_for_status()
            text_init = response_init.json()
            logger.info(f"Ответ инициализации покупки: {text_init}")
            
        except (requests.RequestException, json.JSONDecodeError) as e:
            error_msg = f"Ошибка при инициализации покупки Stars: {e}"
            logger.error(error_msg)
            return False, error_msg
        
        req_id = text_init.get('req_id')
        try:
            amount = float(text_init.get('amount', 0))
            logger.info(f"Требуемая сумма: {amount} TON")
        except (TypeError, ValueError):
            amount = 0
            logger.error("Не удалось конвертировать 'amount' в float.")
        
        if not req_id or amount == 0:
            error_msg = f"Не удалось получить req_id или amount: {text_init}"
            logger.error(error_msg)
            return False, error_msg
        
        # Get purchase link
        payload_link = {
            "account": '{"address":"0:adc5b49f73e4796ecc3c290ad0d89f87fa552b515d173d5295469df9612c24a","chain":"-239","walletStateInit":"te6ccgECFgEAAwQAAgE0AQIBFP8A9KQT9LzyyAsDAFEAAAAAKamjF5hE%2BFriD8Ufe710n9USsAZBzBxLOlXNYCYDiPBRvJZXQAIBIAQFAgFIBgcE%2BPKDCNcYINMf0x%2FT%2F%2FQE0VFDuvKhUVG68qIF%2BQFUEGT5EPKj%2BAAkpMjLH1JAyx9SMMv%2FUhD0AMntVPgPAdMHIcAAn2xRkyDXSpbTB9QC%2BwDoMOAhwAHjACHAAuMAAcADkTDjDQOkyMsfEssfy%2F8SExQVAubQAdDTAyFxsJJfBOAi10nBIJJfBOAC0x8hghBwbHVnvSKCEGRzdHK9sJJfBeAD%2BkAwIPpEAcjKB8v%2FydDtRNCBAUDXIfQEMFyBAQj0Cm%2BhMbOSXwfgBdM%2FyCWCEHBsdWe6kjgw4w0DghBkc3RyupJfBuMNCAkCASAKCwB4AfoA9AQw%2BCdvIjBQCqEhvvLgUIIQcGx1Z4MesXCAGFAEywUmzxZY%2BgIZ9ADLaRfLH1Jgyz8gyYBA%2BwAGAIpQBIEBCPRZMO1E0IEBQNcgyAHPFvQAye1UAXKwjiOCEGRzdHKDHrFwgBhQBcsFUAPPFiP6AhPLassfyz%2FJgED7AJJfA%2BICASAMDQBZvSQrb2omhAgKBrkPoCGEcNQICEekk30pkQzmkD6f%2BYN4EoAbeBAUiYcVnzGEAgFYDg8AEbjJftRNDXCx%2BAA9sp37UTQgQFA1yH0BDACyMoHy%2F%2FJ0AGBAQj0Cm%2BhMYAIBIBARABmtznaiaEAga5Drhf%2FAABmvHfaiaEAQa5DrhY%2FAAG7SB%2FoA1NQi%2BQAFyMoHFcv%2FydB3dIAYyMsFywIizxZQBfoCFMtrEszMyXP7AMhAFIEBCPRR8qcCAHCBAQjXGPoA0z%2FIVCBHgQEI9FHyp4IQbm90ZXB0gBjIywXLAlAGzxZQBPoCE8tqEszMyXP7AMhAFIEBCPRR8qcCAHCBAQjXGPoA0z%2FIVCBHgQEI9FHyp4IQZHN0cnB0gBjIywXLAlAFzxZQA%2FoCE8tqyx8Syz%2FJc%2FsAAAr0AMntVA%3D%3D"}',
            "device": '{"platform":"android","appName":"Tonkeeper","appVersion":"5.0.18","maxProtocolVersion":2,"features":["SendTransaction",{"name":"SendTransaction","maxMessages":4}]}',
            "transaction": "1",
            "id": req_id,
            "show_sender": self.config.get("SHOW_SENDER", "0"),
            "method": "getBuyStarsLink"
        }
        
        try:
            response_link = requests.post(api_url, headers=self.headers, data=payload_link)
            response_link.raise_for_status()
            text_link = response_link.json()
            logger.info(f"Ответ получения ссылки на покупку: {text_link}")
            
        except (requests.RequestException, json.JSONDecodeError) as e:
            error_msg = f"Ошибка при получении ссылки на покупку Stars: {e}"
            logger.error(error_msg)
            return False, error_msg
        
        if not text_link.get('ok'):
            error_msg = f"Ошибка при получении ссылки на покупку Stars: {text_link.get('error', 'Unknown error')}"
            logger.error(error_msg)
            return False, error_msg
            
        transaction_messages = text_link.get('transaction', {}).get('messages', [])
        if not transaction_messages:
            error_msg = f"Сообщения транзакции не найдены: {text_link}"
            logger.error(error_msg)
            return False, error_msg
        
        payload_transaction = transaction_messages[0].get('payload')
        if not payload_transaction:
            error_msg = f"Payload сообщения транзакции не найден: {text_link}"
            logger.error(error_msg)
            return False, error_msg
        
        try:
            decoded_payload = self._decode_payload(payload_transaction)
            ref_id = self._extract_ref_id(data=decoded_payload)
            comment = f"{quantity} Telegram Stars \n\nRef#{ref_id}"
            logger.info(f"Комментарий для транзакции: {comment}")
        except Exception as e:
            error_msg = f"Ошибка при обработке payload транзакции: {e}"
            logger.error(error_msg)
            return False, error_msg
        
        try:
            tx_hash, ref_id, error_transaction = await self.send_ton_transaction(amount, comment)
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

async def main():
    """Example usage of FragmentAPI."""
    api = FragmentAPI()  # You can pass custom config here if needed

    if api.config["fragment_api"]["hash"] == "YOUR_FRAGMENT_HASH" or api.config["fragment_api"]["cookie"] == "YOUR_FRAGMENT_COOKIE":
        print("❌ Необходимо настроить Fragment API!")
        print("Установите правильные значения для hash и cookie")
        return

    print("⭐️ AutoStars - Покупка Stars через Fragment API")
    print("=" * 50)

    print("💰 Проверяем баланс кошелька...")
    balance = await api.check_wallet_balance()
    print(f"Баланс: {balance} TON")

    if balance < 0.1:
        print(f"❌ Недостаточно средств на кошельке! Баланс: {balance} TON")
        print("Для покупки Stars необходимо пополнить кошелек минимум на 0.1 TON")
        return

    print("\n📝 Введите данные для покупки:")
    username = input("Имя пользователя (с @ или без): ").strip()
    if not username:
        print("❌ Имя пользователя не может быть пустым!")
        return

    min_stars = api.config.get("MIN_STARS", 50)
    max_stars = api.config.get("MAX_STARS", 1000000)
    print(f"Введите количество Stars (от {min_stars} до {max_stars}):")
    try:
        quantity = int(input("Количество Stars: "))
    except ValueError:
        print("❌ Количество должно быть числом!")
        return

    print(f"\n🔄 Покупаем {quantity} Stars для {username}...")
    success, message = await api.buy_stars(username, quantity)

    if success:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
