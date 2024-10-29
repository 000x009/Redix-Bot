import re
from typing import Any, Optional

from pydantic import BaseModel, field_validator, AnyUrl


class NewReferralCode(BaseModel):
    referral_code: str


class ReferralCode(BaseModel):
    code: str
    referral_url: AnyUrl
