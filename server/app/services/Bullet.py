import time
import uuid
from app.utils import Vector2


class Bullet:
    def __init__(self, owner_id: str, x: float, y: float, vel: Vector2.Vector2) -> None:
        self.id = str(uuid.uuid4())[:8]
        self.owner = owner_id
        self.x = x
        self.y = y
        self.velocity = vel
        self.health = 100.0
        self.spawn_time = time.time()
