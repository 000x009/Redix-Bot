from typing import Literal

import requests

_GameLiteral = Literal['laser', 'magic', 'scroll']


class SupercellAuthService():
    def __init__(self) -> None:
        self.base_url = 'https://id.supercell.com/api'
        self.headers = None
    
    def login(self, email: str, game: _GameLiteral) -> None:
        url = "https://bs.rldv1.dev/scid/requestCode"
        params = {
            "key": "8d436516fb5c548433488f2d25bc9d2f",
            "mail": f"{email}"
        }

        response = requests.get(url, params=params)

        return response
    
    def code_validate(self, email: str, code: str) -> tuple[bool, str]:
        pin_data = {"email": email, "pin": code}
        req = requests.post(url=f'{self.base_url}/ingame/account/login.confirm', data=pin_data, headers=self.headers)
        content = req.json()
        ok = content.get('ok')
        error = content.get('error')

        return ok, error
    