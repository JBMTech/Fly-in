*This project has been created as part of the 42 curriculum by jabuleje*

# ✈️ Fly-in

## 📖 Description

Fly-in is a Python project developed as part of the 42 curriculum. It simulates drone routing through a network of connected zones, with the objective of transporting drones from a starting zone to a destination zone while minimizing the number of turns required.

The environment is represented as a graph. Zones are the graph's nodes, and connections between zones are its edges. Each zone can have different properties, such as a maximum drone capacity or a specific zone type. Connections can also have capacity restrictions.

The project combines graph representation, pathfinding algorithms, resource constraints, and a graphical simulation.

## 🎯 Main objectives

- Parse and validate map files.
- Represent the environment using a graph.
- Find suitable paths between the starting zone and the destination.
- Account for different zone types and movement costs.
- Simulate drone movements while respecting zone and connection capacities.
- Visualize the graph and drone movements using Pygame.

## ✨ Features

- **Map parsing:** Reads map definitions containing the number of drones, zones, coordinates, metadata, and connections.
- **Graph representation:** Stores zones, connections, and adjacency relationships.
- **Pathfinding:** Uses the A* search algorithm to find routes to the destination.
- **Zone types:** Supports normal, restricted, priority, and blocked zones.
- **Capacity constraints:** Supports maximum drone occupancy per zone and maximum capacity per connection.
- **Drone simulation:** Models drone movements along their assigned paths.
- **Graphical visualization:** Displays zones, connections, drones, and the current simulation turn.

## 🛠️ Instructions

### 📋 Requirements

- Python 3.10 or later.
- `uv` for Python environment and dependency management.
- Project dependencies declared in the project configuration, including Pygame and the development tools used for code quality checks.
- A compatible graphical environment for running the Pygame visualization.

### ⚙️ Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd <repository-directory>
```

Install the project dependencies:

```bash
make install
```

### ▶️ Execution

Run the simulation with a map file:

```bash
make run MAP=maps/easy/02_simple_fork.txt
```

The program parses and validates the map, builds the graph, searches for candidate routes, and launches the graphical simulation.

#### Available Makefile commands

```bash
make install       # Install dependencies
make run           # Run the simulation
make debug         # Run under the Python debugger
make lint          # Run flake8 and mypy
make lint-strict   # Run stricter static checks
make clean         # Remove cache files
make fclean        # Remove caches and the virtual environment
make help          # Display available commands
```

### 🗺️ Map format

Map files describe the number of drones, the zones, and the connections between them.

**Example:**

```text
nb_drones: 4
start_hub: start 0 0
hub: junction 1 0
hub: path_a 2 1
hub: path_b 2 -1
end_hub: goal 3 0
connection: start-junction
connection: junction-path_a
connection: path_a-goal
connection: junction-path_b
connection: path_b-goal
```

The exact metadata syntax and validation rules are implemented by the parser.

## 🧠 Algorithm and implementation strategy

### 1. Graph representation

- **Zone:** Represents a location and stores its name, coordinates, type, color, maximum capacity, and drones currently occupying it.
- **Connection:** Represents a link between two zones and stores its capacity.
- **Graph:** Maintains the collection of zones, connections, adjacency lists, and connection lookups.

The adjacency list allows the pathfinding algorithm to retrieve the neighbors of a given zone efficiently.

### 2. Pathfinding with A*

The project uses the A* search algorithm to find a route between the starting zone and the destination.

A* evaluates candidate zones using the following function:

```text
f(n) = g(n) + h(n)
```

Where:

- `g(n)` is the accumulated movement cost from the starting zone to the current zone.
- `h(n)` is a heuristic estimate of the remaining cost to the destination.
- `f(n)` is the estimated total cost used to prioritize the search.

The implementation uses Manhattan distance as the basis for its heuristic. Since movement costs vary according to zone type, the heuristic must be compatible with the movement costs and map structure to preserve A*'s optimality guarantees.

Movement costs are assigned according to the destination zone's type:

| Zone type | Pathfinding cost | Meaning |
|:---:|:---:|---|
| Normal | 1.0 | Standard movement cost |
| Priority | 0.5 | Lower pathfinding cost |
| Restricted | 2.0 | Higher pathfinding cost |
| Blocked | Infinite | The zone cannot be entered |

### 3. Candidate route generation

The `find_smart_paths()` method repeatedly runs A* while increasing penalties for intermediate zones used by previously discovered routes.

This encourages the search to explore alternative routes. The method removes duplicate paths, ranks the candidates by their original movement costs, and selects up to two candidate routes.

This is a heuristic route-generation strategy. It does not guarantee that every possible route is found or that the selected pair is globally optimal for minimizing the total simulation time.

### 4. Drone simulation and capacity management

The `Simulation` class assigns routes to drones and advances their movements turn by turn.

Before a drone moves, the simulation checks whether the corresponding connection has available capacity and whether the destination zone can accept another drone. Drones that cannot move must wait for a later turn.

Restricted zones require additional movement handling. The simulation records drone positions and movement history so that the graphical interface can display the evolution of the network.

The total number of turns depends on the selected routes, the number of drones, zone capacities, connection capacities, and the coordination of movements.

### 5. Graphical visualization

The project uses Pygame to display the graph and its current state.

The visualization includes:

- **Zones:** Drawn as circles at their map coordinates.
- **Connections:** Drawn as lines linking connected zones.
- **Drones:** Represented by circles around the zones they occupy.
- **Turn counter:** Displays the current simulation turn.
- **Step-by-step execution:** Use the right arrow key to advance the simulation, if supported by the current implementation.

The graphical interface helps users understand the graph topology, observe drone distribution, and follow the simulation one turn at a time.

## 📚 Resources

### 📝 Documentation and references

- [Python Documentation](https://docs.python.org/3/)
- [Python `heapq` Documentation](https://docs.python.org/3/library/heapq.html)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Explanation of A*(YouTube)](https://www.youtube.com/watch?v=hQa9JTtq4Ok)
- [A* Tutorial (DataCamp)](https://www.datacamp.com/tutorial/a-star-algorithm)
- [A* Search Algorithm — Red Blob Games](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Graph Theory — NetworkX Documentation](https://networkx.org/documentation/stable/tutorial.html)

These resources were used as references for Python development, priority queues, graph representation, pathfinding concepts, and graphical rendering.

### 🤖 AI usage

AI tools were used as a learning and development aid during the project.

Their use included:

- Explaining graph theory and pathfinding concepts, including A*.
- Helping identify potential bugs and edge cases in Python code.
- Explaining Python classes, type hints, and interactions between modules.
- Assisting with the design and debugging of the Pygame visualization.
