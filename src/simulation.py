from typing import List

from .graph import Graph
from .drone import Drone
from .zone import Zone


class Simulation:

    def __init__(
        self,
        graph: Graph,
        paths: List[List[Zone]],
        nb_drones: int
    ) -> None:

        self.graph = graph
        self.paths = paths
        self.nb_drones = nb_drones

        self.drones: List[Drone] = []

        self.turn = 0

    def initialize_drones(self) -> None:

        if self.drones:
            return

        start = self.graph.start_zone

        if start is None:
            return

        if not self.paths:
            return

        for i in range(self.nb_drones):

            path = self.paths[i % len(self.paths)]

            drone = Drone(
                f"D{i + 1}",
                path
            )

            self.drones.append(drone)

            start.drones.append(drone)

    def can_move(self, drone: Drone) -> bool:

        if drone.finished():
            return False

        current = drone.current_zone()

        next_zone = drone.path[
            drone.current_point + 1
        ]

        connection = self.graph.get_connection(
            current.name,
            next_zone.name
        )

        if connection is None:
            return False

        if connection.drones_on_link >= connection.capacity:
            return False

        if next_zone == self.graph.end_zone:
            return True

        if len(next_zone.drones) >= next_zone.max_drones:
            return False

        return True

    def simulate_turn(self) -> None:

        for connection in self.graph.connections:
            connection.drones_on_link = 0

        moved = False

        active_drones = [
            drone
            for drone in self.drones
            if not drone.finished()
        ]

        active_drones.sort(
            key=lambda drone: drone.current_point,
            reverse=True
        )

        for drone in active_drones:

            if drone.in_transit:

                next_zone = drone.path[
                    drone.current_point + 1
                ]

                next_zone.drones.append(drone)

                drone.move()

                drone.in_transit = False

                moved = True

                continue

            if not self.can_move(drone):
                continue

            current = drone.current_zone()

            next_zone = drone.path[
                drone.current_point + 1
            ]

            connection = self.graph.get_connection(
                current.name,
                next_zone.name
            )

            if connection is None:
                continue

            if next_zone.zone_type == "restricted":

                current.drones.remove(drone)

                drone.in_transit = True

                connection.drones_on_link += 1

                moved = True

                continue

            current.drones.remove(drone)

            next_zone.drones.append(drone)

            drone.move()

            connection.drones_on_link += 1

            moved = True

        if moved:
            self.turn += 1

    def all_finished(self) -> bool:

        return all(
            drone.finished()
            for drone in self.drones
        )