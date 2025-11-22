from typing import Any


class Player:
    def __init__(self, pid: str, name: str) -> None:
        self.id = pid
        self.name = name
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0
        self.health = 100.0
        self.last_input_seq = 0
        self.inputs: list[Any] = []  # queue for inputs
