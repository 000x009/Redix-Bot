from dataclasses import dataclass, field


@dataclass()
class Category:
    id: int
    game_id: int
    name: str
    image: str = field(default=None)
    is_visible: bool = field(default=True)
    thread_id: int = field(default=None)
    web_app_place: int = field(default=None)
