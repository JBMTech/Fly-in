import heapq
from typing import Dict, List, Tuple
from .zone import Zone
from .graph import Graph


class Pathfinding:

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def heuristic(self, zone: Zone) -> int:
        """
        Estimate the distance from zone to the goal.
        """

        goal = self.graph.end_zone

        return abs(zone.x - goal.x) + abs(zone.y - goal.y)

    def movement_cost(self, zone: Zone) -> int:
        """
        Return the cost of entering a zone.
        """

        if zone.zone_type == "restricted":
            return 3

        return 1

    def find_path(self) -> List[Zone]:
        """
        Find the lowest-cost path from start_zone
        to end_zone using A*.
        """

        start = self.graph.start_zone
        goal = self.graph.end_zone

        if start is None or goal is None:
            return []

        open_set: List[Tuple[int, int, Zone]] = []

        counter = 0

        heapq.heappush(
            open_set,
            (0, counter, start)
        )

        g_score: Dict[Zone, int] = {
            start: 0
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

                # Blocked zones cannot be used.
                if neighbor.zone_type == "blocked":
                    continue

                movement_cost = self.movement_cost(
                    neighbor
                )

                tentative_g_score = (
                    g_score[current]
                    + movement_cost
                )

                if (
                    neighbor not in g_score
                    or tentative_g_score < g_score[neighbor]
                ):

                    came_from[neighbor] = current

                    g_score[neighbor] = (
                        tentative_g_score
                    )

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
        self,
        came_from: Dict[Zone, Zone],
        current: Zone
    ) -> List[Zone]:

        path = [current]

        while current in came_from:

            current = came_from[current]

            path.append(current)

        path.reverse()

        return path
