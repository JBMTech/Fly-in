from typing import List
from .graph import Graph
from .drone import Drone
from .zone import Zone


class Simulation:

    def __init__(
        self,
        graph: Graph,
        path: List[Zone],
        nb_drones: int
    ) -> None:

        self.graph = graph
        self.path = path
        self.nb_drones = nb_drones
        self.drones: List[Drone] = []
        self.turn = 0

    def initialize_drones(self) -> None:

        start = self.graph.start_zone

        if start is None:
            return

        for i in range(1, self.nb_drones + 1):

            drone = Drone(
                f"D{i}",
                self.path
            )

            self.drones.append(drone)
            start.drones.append(drone)

    def can_move(self, drone: Drone) -> bool:

        if drone.finished():
            return False

        next_zone = drone.path[
            drone.current_point + 1
        ]

        if next_zone == self.graph.end_zone:
            return True

        if len(next_zone.drones) >= next_zone.max_drones:
            return False

        return True

    def simulate_turn(self) -> None:

        self.turn += 1

        for drone in self.drones:

            if drone.finished():
                continue

            if not self.can_move(drone):
                continue

            current = drone.current_zone()

            next_zone = drone.path[
                drone.current_point + 1
            ]

            current.drones.remove(drone)
            next_zone.drones.append(drone)

            drone.move()

    def all_finished(self) -> bool:

        return all(
            drone.finished()
            for drone in self.drones
        )