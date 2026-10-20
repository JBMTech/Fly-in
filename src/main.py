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


def valid_arg(*args: str) -> str | Tuple[str, str]:
    """Validate the command-line arguments and return the map file path."""
    if len(sys.argv) == 2:
        return sys.argv[1]
    elif len(sys.argv) == 3 and args[2] == "--capacity-info":
        return args[1], args[2]
    else:
        print("Usage: make run MAP=<map_file>")
        sys.exit(1)


def main() -> None:
    """
    Parse the map, find suitable paths, and
    run the drone simulation with visualization.
    """
    if isinstance(valid_arg, str):
        file_map = valid_arg()
    elif isinstance(valid_arg, tuple):
        file_map, info = valid_arg()
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

        if info:
            simulation = Simulation(
                graph,
                paths,
                parser.nb_drones,
                True
            )
        else:
            simulation = Simulation(
                graph,
                paths,
                parser.nb_drones,
                False
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
