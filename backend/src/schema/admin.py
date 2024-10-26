from typing import List
from dataclasses import dataclass

from src.data.models.admin import AdminRole


@dataclass
class Admin:
    id: int
    user_id: int
    role: AdminRole
    permissions: dict[str, bool]
