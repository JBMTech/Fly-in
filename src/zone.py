from typing import List
from drone import Drone


class Zone:

    def __init__(self,
                 name: str,
                 x: int,
                 y: int,
                 max_drones: int = 1,
                 color: str = "none",
                 zone_type: str = "normal") -> None:
        self.name = name
        self.x = x
        self.y = y
        self.max_drones = max_drones
        self.color = color
        self.zone_type = zone_type

        self.drones: List[Drone] = []

    