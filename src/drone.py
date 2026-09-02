from typing import List, Any



class Drone:

    def __init__(
        self,
        drone_id: str,
        path: List[Any]
    ) -> None:

        self.id = drone_id
        self.path = path
        self.current_point = 0

    def current_zone(self) -> Any:
        return self.path[self.current_point]

    def move(self) -> bool:

        if self.current_point + 1 >= len(self.path):
            return False

        self.current_point += 1
        return True

    def finished(self) -> bool:

        return self.current_point >= len(self.path) - 1