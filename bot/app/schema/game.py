from dataclasses import dataclass, field

@dataclass()
class Game:
    id: int
    name: str
    image_url: str
    web_app_place: int
    supergroup_id: int = field(default=None)

