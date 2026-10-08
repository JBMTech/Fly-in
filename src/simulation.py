
from typing import List, Dict, Tuple, Set, Any

from .graph import Graph
from .drone import Drone
from .zone import Zone


# One snapshot contains the state of the graph at a given turn.
Snapshot = Tuple[
    Dict[str, List[str]],
    Dict[Tuple[str, str], List[str]],
    Dict[str, int],
    Dict[Tuple[str, str], int]
]


class Simulation:
    """Manage drone movements and store simulation history."""

    def __init__(
        self,
        graph: Graph,
        paths: List[List[Zone]],
        nb_drones: int,
        flag: bool = False
    ) -> None:

        self.graph = graph
        self.paths = paths
        self.nb_drones = nb_drones
        self.flag = flag

        self.drones: List[Drone] = []
        self.turn = 0

        # Drones currently travelling to a restricted zone.
        self.delayed_drones: Set[str] = set()

        # State history for the visualizer.
        self.history: List[Snapshot] = []

        # Movement log for each turn.
        self.moves_history: List[List[str]] = []

        # Initialize drones and record the initial state.
        self.initialize_drones()
        self.history.append(self.capture_snapshot())

    def initialize_drones(self) -> None:
        """Place drones at the starting zone."""

        if self.drones or not self.paths:
            return

        start = self.graph.start_zone

        if start is None:
            return

        for i in range(self.nb_drones):
            path = self.paths[i % len(self.paths)]

            if not path:
                continue

            drone = Drone(f"D{i + 1}", path)
            self.drones.append(drone)
            start.drones.append(drone)

    def reserved_drones(self, zone: Zone) -> int:
        """Count drones travelling to a zone but not yet inside it."""

        count = 0

        for drone in self.drones:
            if not drone.in_transit or drone.finished():
                continue

            next_zone = drone.path[drone.current_point + 1]

            if next_zone == zone:
                count += 1

        return count

    def can_move(self, drone: Drone) -> bool:
        """Check connection and destination capacity."""

        if drone.finished():
            return False

        current = drone.current_zone()
        next_zone = drone.path[drone.current_point + 1]

        connection = self.graph.get_connection(
            current.name,
            next_zone.name
        )

        if connection is None:
            return False

        if connection.drones_on_link >= connection.capacity:
            return False

        if next_zone != self.graph.end_zone:
            occupied = (
                len(next_zone.drones)
                + self.reserved_drones(next_zone)
            )

            if occupied >= next_zone.max_drones:
                return False

        return True

    def capture_snapshot(self) -> Snapshot:
        """Capture the positions and occupancy of all drones."""

        drones_by_zone: Dict[str, List[str]] = {}
        drones_on_links: Dict[Tuple[str, str], List[str]] = {}

        for drone in self.drones:

            if drone.finished():
                zone = self.graph.end_zone

                if zone is not None:
                    drones_by_zone.setdefault(
                        zone.name, []
                    ).append(drone.id)

                continue

            current = drone.current_zone()

            if drone.in_transit:
                next_zone = drone.path[
                    drone.current_point + 1
                ]

                link = (current.name, next_zone.name)

                drones_on_links.setdefault(
                    link, []
                ).append(drone.id)

            else:
                drones_by_zone.setdefault(
                    current.name, []
                ).append(drone.id)

        zone_counts = {
            name: len(zone.drones) + self.reserved_drones(zone)
            for name, zone in self.graph.zones.items()
        }

        link_counts = {
            (connection.zone1, connection.zone2):
                connection.drones_on_link
            for connection in self.graph.connections
        }

        return (
            drones_by_zone,
            drones_on_links,
            zone_counts,
            link_counts
        )

    def simulate_turn(self) -> bool:
        """Execute one turn and save its state."""

        for connection in self.graph.connections:
            connection.drones_on_link = 0

        active_drones = [
            drone for drone in self.drones
            if not drone.finished()
        ]

        # Prioritize drones that have advanced further.
        active_drones.sort(
            key=lambda drone: drone.current_point,
            reverse=True
        )

        moves_this_turn: List[str] = []

        for drone in active_drones:

            current = drone.current_zone()
            next_zone = drone.path[
                drone.current_point + 1
            ]

            connection = self.graph.get_connection(
                current.name,
                next_zone.name
            )

            # Complete a movement started on the previous turn.
            if drone.in_transit:

                if drone in current.drones:
                    current.drones.remove(drone)

                next_zone.drones.append(drone)
                drone.move()
                drone.in_transit = False
                self.delayed_drones.discard(drone.id)

                moves_this_turn.append(
                    f"{drone.id}-{next_zone.name}"
                )

                continue

            if not self.can_move(drone):
                continue

            if connection is None:
                continue

            if next_zone.zone_type == "restricted":

                if drone in current.drones:
                    current.drones.remove(drone)

                drone.in_transit = True
                self.delayed_drones.add(drone.id)

                connection.drones_on_link += 1

                moves_this_turn.append(
                    f"{drone.id}-{current.name}-{next_zone.name}"
                )

                continue

            # Normal movement.
            if drone in current.drones:
                current.drones.remove(drone)

            next_zone.drones.append(drone)
            drone.move()

            connection.drones_on_link += 1

            move = f"{drone.id}-{next_zone.name}"

            if self.flag and next_zone != self.graph.end_zone:
                move += (
                    f"-{len(next_zone.drones)}"
                    f"/{next_zone.max_drones}"
                )

            moves_this_turn.append(move)

        # Do not create an endless loop if no drone can progress.
        if not moves_this_turn:
            return False

        self.turn += 1

        self.moves_history.append(moves_this_turn)
        self.history.append(self.capture_snapshot())

        print(" ".join(moves_this_turn))

        return True

    def all_finished(self) -> bool:
        """Return True when every drone has arrived."""

        return all(
            drone.finished()
            for drone in self.drones
        )

    def run(self) -> None:
        """Run the simulation until completion or a deadlock."""

        while not self.all_finished():

            moved = self.simulate_turn()

            if not moved:
                print(
                    "Simulation stopped: "
                    "no drones can move."
                )
                break

        print(f"Simulation finished in {self.turn} turns.")
