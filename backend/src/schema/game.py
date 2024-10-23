from dataclasses import dataclass, field

@dataclass()
class Game:
    id: int
    name: str
    image_url: str
    supergroup_id: int = field(default=None)

