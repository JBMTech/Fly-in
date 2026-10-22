import sys

from typing import Tuple
from .parsing import Parser
from .graph import Graph
from .simulation import Simulation
from .visualizer import Visualizer
from .pathfinding import Pathfinding
from .exceptions import ParsingError

_RED = "\033[31m"
_RESET = "\033[0m"


class Argument:

    def __init__(self, argv: list[str]) -> None:
        self.argv = argv

    def valid_arg(self) -> Tuple[str, bool]:
        """Validate command-line arguments."""

        args = self.argv[1:]
        capacity_info = "--capacity-info" in args

        if capacity_info:
            args.remove("--capacity-info")

        if len(args) != 1:
            print(
                f"{_RED}[ERROR]{_RESET} Usage: make run MAP=<map_file> "
                "[ARGS=--capacity-info]"
            )
            sys.exit(1)

        return args[0], capacity_info


def main() -> None:
    """
    Parse the map, find suitable paths, and
    run the drone simulation with visualization.
    """
    arg = Argument(sys.argv)
    file_map, info = arg.valid_arg()

    parser = Parser(file_map)

    try:
        parser.parsing()
        graph: Graph = parser.graph

        print("\n==================== INFO ========================")
        print(f"Total Drones : {parser.nb_drones}")
        print(f"Total conection: {len(parser.connections)}")
        print(f"Start Zone   : {graph.start_zone.name}")
        print(f"End Zone     : {graph.end_zone.name}")
        print("====================================================")

        pathfinding = Pathfinding(graph)

        paths = pathfinding.find_smart_paths(
            parser.nb_drones
        )

        if not paths:
            print("No path found.")
            return

        print("\n====================== PATHS =======================")

        for index, path in enumerate(paths, start=1):
            names = [zone.name for zone in path]
            print(f"Path {index}: {' -> '.join(names)}")

        print("====================================================")

        simulation = Simulation(
            graph,
            paths,
            parser.nb_drones,
            info
        )

        visualizer = Visualizer(
            graph,
            simulation
        )

        print("\n================ SIMULATION ========================")

        visualizer.run()

        print("====================================================")

    except ParsingError as ex:
        print(
            f"{_RED}[ERROR]{_RESET} {ex}"
        )


if __name__ == "__main__":
    main()
