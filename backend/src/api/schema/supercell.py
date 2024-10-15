from typing import Literal

from pydantic import BaseModel, EmailStr


class SupercellAuthDTO(BaseModel):
    email: EmailStr
    game: Literal['laser', 'scroll', 'magic', 'soil']
    