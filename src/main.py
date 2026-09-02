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
        print(f"Start Zone   : {graph.start_zone.name}")
        print(f"End Zone     : {graph.end_zone.name}")
        print("=======================================================")

        pathfinding = Pathfinding(graph)

        path = pathfinding.find_path()

        simulation = Simulation(
            graph,
            path,
            parser.nb_drones
        )

        simulation.initialize_drones()

        visualizer = Visualizer(
            graph,
            simulation
        )

        visualizer.run()


        if not path:
            print("No path found.")
            return

        print("Path found:")

        print("\n====================== PATH =======================")

        for zone in path:
            print(zone.name)

        print("====================================================")


    except ParsingError as ex:
        print(f"[ERROR]: {ex}")


if __name__ == "__main__":
    main()