from typing import Literal
import requests
import hmac
import base64
import urllib.parse
import requests
import time

_GameLiteral = Literal['laser', 'magic', 'scroll']


class SupercellAuthService():
    def __init__(self) -> None:
        self.base_url = 'https://id.supercell.com/api'
        self.headers = None
        self.keychain = {
            "magic": self.shuffle(bytes.fromhex("ad161215d2216483441a3fc5ba0f18b108441584ba888e0f66d43a38f870c1b9"), 42),
            "laser": self.shuffle(bytes.fromhex("4d5875b5afc4aee2cffa68dfe5788d730e602e1cb6061ff3c3cb5ba37bd4bf58"), 42),
            "squad": self.shuffle(bytes.fromhex("91128e16c76fd026366b5f10648d46240777d8d4fcf0b1287b796fa8e1056499"), 42),
            "soil": self.shuffle(bytes.fromhex("dd68010d2bec62c63fe89d562c07673d6f15ea3ef033a2814d3251157de55c46"), 42),
            "scroll": self.shuffle(bytes.fromhex("884e0665320eca797ac8bfed384b485b84039b441cbd0995483a796569eff170"), 42),
            "reef": self.shuffle(bytes.fromhex("c4957427c7657c14c92242aa67db1324875335ef027717640926785c4a36fb28"), 42),
        }
    
    def login(self, email: str, game: _GameLiteral) -> None:
        ts = int(time.time())
        host = "https://id.supercell.com"
        path = "/api/ingame/account/login"
        body = urllib.parse.urlencode({
            "lang": "en",
            "email": email,
            "remember": "true",
            "game": game,
            "env": "prod",
            "unified_flow": "LOGIN",
            "recaptchaToken": "FAILED_EXECUTION",
            "recaptchaSiteKey": "6Lf3ThsqAAAAABuxaWIkogybKxfxoKxtR-aq5g7l"
        })
        headers = {
            "User-Agent": f"scid/1.5.8-f (iPadOS 18.1; {game}-prod; iPad8,6) com.supercell.{game}/59.197",
            "Accept-Language": "en",
            "Accept-Encoding": "gzip",
            "X-Supercell-Device-Id": "1E923809-1680-535C-80F0-EFEFEFEFEF38", 
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Content-Length": str(len(body)),
            "Accept": None,
            "Connection": None
        }

        headers["X-Supercell-Request-Forgery-Protection"] = self.sign(ts, path, "POST", body, headers, game)

        result = requests.post(f"{host}{path}", headers={k.lower(): v for k, v in headers.items()}, data=body)

        return result.json()

    def shuffle(self, base: bytes, seed: int) -> bytes:
        size = len(base)
        numbers = list(range(size))
        x = seed
        for i in range(size):
            j = (size - 1) - i
            # type(x) is uint32
            x = (0x19660D * x + 0x3C6EF35F) & 0xFFFFFFFF
            k = x % (j + 1)
            # swap the elements
            v = numbers[j]
            numbers[j] = numbers[k]
            numbers[k] = v
        offsets = [0] * size
        for i in range(size):
            offsets[numbers[i]] = i
        result = [0] * size
        for i in range(size):
            result[i] = base[offsets[i]]
        return bytes(result)

    def sign(self, timestamp: int, path: str, method: str, body: str, headers: dict[str, str], game: str) -> str:
        key = self.keychain.get(game)
        headers_str = ""
        headers_value_str = ""
        for header in ("Authorization", "User-Agent", "X-Supercell-Device-Id"):
            if header in headers:
                header_lower = header.lower()
                if len(headers_str) > 0:
                    headers_str += ";"
                headers_str += header_lower
                headers_value_str += header_lower + "=" + headers[header]

        to_sign = f"{timestamp}{method}{path}{body}{headers_value_str}"
        x = hmac.digest(key, to_sign.encode("utf-8"), "sha256")
        xb = base64.b64encode(x).decode("utf-8").replace("+", "-").replace("/", "_").replace("=", "")
        return f"RFPv1 Timestamp={timestamp},SignedHeaders={headers_str},Signature={xb}"
    
    def code_validate(self, email: str, code: str) -> tuple[bool, str]:
        pin_data = {"email": email, "pin": code}
        req = requests.post(url=f'{self.base_url}/ingame/account/login.confirm', data=pin_data, headers=self.headers)
        content = req.json()
        ok = content.get('ok')
        error = content.get('error')

        return ok, error
    