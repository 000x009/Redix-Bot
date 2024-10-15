from typing import Mapping, Sequence, Optional, Literal
from dataclasses import dataclass, field


@dataclass(frozen=True)
class User:
    user_id: int
    referral_code: str
    referral_id: int = field(default=None)
    balance: float = field(default=0)
    used_coupons: Optional[Mapping[Literal['coupons'], Sequence]] = field(default=None)
    nickname: Optional[str] = field(default=None)
    profile_photo: Optional[str] = field(default=None)
