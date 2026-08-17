from typing import List, Any


class Drone:
    def __init__(self, drone_id: str, path: List[Any]):
        self.id = drone_id
        self.path = path
        self.current_point = 0