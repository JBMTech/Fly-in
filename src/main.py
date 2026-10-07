import sys

from .parsing import Parser
from .graph import Graph
from .simulation import Simulation
from .visualizer import Visualizer
from .pathfinding import Pathfinding
from .exceptions import ParsingError


def valid_arg() -> str:
    if len(sys.argv) == 2:
        return sys.argv[1]

    print("Usage: make run MAP=<map_file>")
    sys.exit(1)


def main() -> None:
    file_map = valid_arg()
    parser = Parser(file_map)

    try:
        parser.parsing()
        graph: Graph = parser.graph

        print("\n====================== INFO =========================")
        print(f"Total Drones : {parser.nb_drones}")
        print(f"Total conection: {len(parser.connections)}")
        print(f"Start Zone   : {graph.start_zone.name}")
        print(f"End Zone     : {graph.end_zone.name}")
        print("=======================================================")

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
            parser.nb_drones
        )

        visualizer = Visualizer(
            graph,
            simulation
        )

        visualizer.run()

    except ParsingError as ex:
        print(
            f"[ERROR]: {ex} --> "
            f"Usage: make run MAP=<map_file>"
        )


if __name__ == "__main__":
    main()
