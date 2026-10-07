import heapq
from typing import Dict, List, Tuple

from .zone import Zone
from .graph import Graph


class Pathfinding:

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def heuristic(self, zone: Zone) -> float:
        goal = self.graph.end_zone

        if goal is None:
            return float("inf")

        return abs(zone.x - goal.x) + abs(zone.y - goal.y)

    def movement_cost(
        self,
        zone: Zone,
        penalties: Dict[Zone, float]
    ) -> float:

        if zone.zone_type == "blocked":
            return float("inf")

        if zone.zone_type == "restricted":
            cost = 2.5
        elif zone.zone_type == "priority":
            cost = 0.5
        else:
            cost = 1.0

        cost += penalties.get(zone, 0.0)

        return cost

    def zone_turn_cost(self, zone: Zone) -> float:

        if zone.zone_type == "blocked":
            return float("inf")

        if zone.zone_type == "restricted":
            return 2.0

        return 1.0

    def find_path(
            self, penalties: Dict[Zone, float] | None = None) -> List[Zone]:

        if penalties is None:
            penalties = {}

        start = self.graph.start_zone
        goal = self.graph.end_zone

        if start is None or goal is None:
            return []

        open_set: List[Tuple[float, int, Zone]] = []

        counter = 0

        heapq.heappush(
            open_set,
            (0.0, counter, start)
        )

        g_score: Dict[Zone, float] = {
            start: 0.0
        }

        came_from: Dict[Zone, Zone] = {}

        while open_set:

            _, _, current = heapq.heappop(open_set)

            if current == goal:
                return self.reconstruct_path(
                    came_from,
                    current
                )

            for neighbor in self.graph.adjacency_list[current]:

                movement_cost = self.movement_cost(
                    neighbor,
                    penalties
                )

                if movement_cost == float("inf"):
                    continue

                tentative_g_score = (
                    g_score[current]
                    + movement_cost
                )

                if (
                    neighbor not in g_score
                    or tentative_g_score < g_score[neighbor]
                ):
                    came_from[neighbor] = current

                    g_score[neighbor] = tentative_g_score

                    f_score = (
                        tentative_g_score
                        + self.heuristic(neighbor)
                    )

                    counter += 1

                    heapq.heappush(
                        open_set,
                        (
                            f_score,
                            counter,
                            neighbor
                        )
                    )

        return []

    def reconstruct_path(
            self, came_from: Dict[Zone, Zone], current: Zone) -> List[Zone]:

        path = [current]

        while current in came_from:
            current = came_from[current]
            path.append(current)

        path.reverse()

        return path

    def find_smart_paths(self, total_drones: int) -> List[List[Zone]]:

        all_unique_paths: List[List[Zone]] = []

        zone_penalties: Dict[Zone, float] = {}

        best_turn_count = float("inf")

        best_paths_combination: List[List[Zone]] = []

        for _ in range(10):

            new_path = self.find_path(
                zone_penalties
            )

            if not new_path:
                break

            for zone in new_path:

                if (
                    zone != self.graph.start_zone
                    and zone != self.graph.end_zone
                ):
                    zone_penalties[zone] = (
                        zone_penalties.get(zone, 0.0)
                        + 0.1
                    )

            if new_path not in all_unique_paths:

                all_unique_paths.append(new_path)

                current_turns = self.calculate_turns(
                    all_unique_paths,
                    total_drones
                )

                if current_turns < best_turn_count:

                    best_turn_count = current_turns

                    best_paths_combination = list(
                        all_unique_paths
                    )

        if best_paths_combination:
            return best_paths_combination

        return all_unique_paths

    def calculate_turns(
        self,
        paths: List[List[Zone]],
        total_drones: int
    ) -> float:

        if not paths:
            return float("inf")

        path_lengths = [
            sum(self.zone_turn_cost(zone)
                for zone in path[1:])
            for path in paths
        ]

        path_lengths.sort()

        shortest_len = path_lengths[0]

        number_of_paths = len(path_lengths)

        diff_sum = sum(
            length - shortest_len
            for length in path_lengths
        )

        if total_drones > diff_sum:

            drones_left = (
                total_drones - diff_sum
            )

            turns = (
                shortest_len
                - 1
                + diff_sum
                + (
                    drones_left
                    + number_of_paths
                    - 1
                ) // number_of_paths
            )

            return float(turns)

        return float(
            shortest_len - 1 + total_drones
        )
