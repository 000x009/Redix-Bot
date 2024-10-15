import re
from typing import Any, Optional

from pydantic import BaseModel, field_validator, AnyUrl


class NewReferralCode(BaseModel):
    referral_code: str

    @classmethod
    @field_validator('referral_code', mode='after')
    def code_validator(cls, v: Any) -> Optional[str]:
        code_sample = r'^[a-zA-Z0-9]+$'
        if type(v) == str and re.match(code_sample, v):
            return v
        
        raise ValueError('Code was entered incorrectly. Accessed only english letters and digits.')


class ReferralCode(BaseModel):
    code: str
    referral_url: AnyUrl
