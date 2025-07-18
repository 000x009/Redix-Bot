from dataclasses import dataclass, field
from typing import List
from uuid import UUID

@dataclass()
class Category:
    id: UUID
    game_id: int
    name: str
    image: str = field(default=None)
    is_visible: bool = field(default=True)
    thread_id: int = field(default=None)
    web_app_place: int = field(default=None)
    required_fields: List[str] = field(default=None)
