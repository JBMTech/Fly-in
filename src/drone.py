from typing import List, Any


class Drone:

    def __init__(
        self,
        drone_id: str,
        path: List[Any]
    ) -> None:
        """Initialize a drone with its identifier, path, and initial state."""

        self.id = drone_id
        self.path = path
        self.current_point = 0
        self.in_transit = False

    def current_zone(self) -> Any:
        """Return the zone where the drone is currently located."""
        return self.path[self.current_point]

    def move(self) -> bool:
        """
        Move the drone to the next point in its path, returning False
        if no further movement is possible.
        """

        if self.current_point + 1 >= len(self.path):
            return False

        self.current_point += 1
        return True

    def finished(self) -> bool:
        """Check whether the drone has reached the end of its path."""
        return self.current_point >= len(self.path) - 1
