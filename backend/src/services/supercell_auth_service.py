from typing import Literal, TypeAlias

import requests

_GameLiteral: TypeAlias = Literal['laser', 'magic', 'scroll']


class SupercellAuthService():
    def __init__(self) -> None:
        self.base_url = 'https://id.supercell.com/api'
        self.headers = None
    
    def login(self, email: str, game: _GameLiteral) -> None:
        self.headers = {
            "User-Agent": f"scid/4543 (Android; {game}-prod)",
            "Authorization": '',
        }
        login_data = {
            "lang": 'en',
            "email": email,
            "remember": "true",
            "game": game,
            "env": "prod",
        }
        requests.post(url=f'{self.base_url}/ingame/account/login', data=login_data, headers=self.headers)
    
    def code_validate(self, email: str, code: str) -> tuple[bool, str]:
        pin_data = {"email": email, "pin": code}
        req = requests.post(url=f'{self.base_url}/ingame/account/login.confirm', data=pin_data, headers=self.headers)
        content = req.json()
        ok = content.get('ok')
        error = content.get('error')

        return ok, error
    