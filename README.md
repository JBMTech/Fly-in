*This project has been created as part of the 42 curriculum by jabuleje*

# Fly-in

## Description

Fly-in is a Python project developed as part of the 42 curriculum. It simulates drone routing through a network of connected zones, with the objective of transporting all drones from a starting zone to a destination zone while minimizing the number of turns required.

The environment is represented as a graph. Zones are the graph's nodes, and connections between zones are its edges. Each zone can have different properties, such as a maximum drone capacity or a specific zone type. Connections can also have capacity restrictions.

The project combines graph representation, pathfinding algorithms, resource constraints, and a graphical simulation.

## Main objectives

* Parse and validate map files.

* Represent the environment using a graph.

* Find suitable paths between the starting zone and the destination.

* Account for different zone types and movement costs.

* Simulate drone movements while respecting zone and connection capacities.

* Visualize the graph and drone movements using Pygame.

## Features

Map parsing: Reads map definitions containing drones, zones, coordinates, metadata, and connections.

Graph representation: Stores zones, connections, and adjacency relationships.

Pathfinding: Uses the A* search algorithm to find routes to the destination.

Zone types: Supports normal, restricted, priority, and blocked zones.

Capacity constraints: Supports maximum drone occupancy per zone and maximum capacity per connection.

Drone simulation: Models drone movements along their assigned paths.

Graphical visualization: Displays zones, connections, drones, and the current simulation turn.

## Instructions

### Requirements

Python 3.10 or later.

uv for Python environment and dependency management.

Pygame and the other dependencies specified in requirements.txt.

A compatible terminal and graphical environment for running the Pygame visualization.

### Installation

Clone the repository and enter the project directory:

````text
git clone <repository-url>
cd <repository-directory>
````

Create the virtual environment and install the dependencies using the project's Makefile:

````text
make install
````

### Execution

Run the simulation with a map file:

````text
make run MAP=maps/easy/02_simple_fork.txt
````

The program parses the map, displays information about the graph, calculates candidate paths, and opens the graphical simulation.

Use the right arrow key to advance the simulation one turn at a time. Close the Pygame window to exit.

### Map format

Map files describe the number of drones, the zones, and the connections between them.

Example:

````text
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
````

The exact metadata syntax and validation rules are implemented by the parser.

## Algorithm and Implementation Strategy

### 1. Graph representation

The environment is modeled as an undirected graph.

* Zone: Represents a location and stores its name, coordinates, type, color, maximum capacity, and drones currently occupying it.

* Connection: Represents a link between two zones and stores its capacity.

* Graph: Maintains the collection of zones, connections, adjacency lists, and connection lookups.

The adjacency list allows the pathfinding algorithm to retrieve the neighbors of a given zone efficiently.

### 2. Pathfinding with A*

The project uses the A* search algorithm to find paths from the starting zone to the destination.

A* evaluates candidate zones using:

````text
f(n) = g(n) + h(n)
````

Where:

  * g(n) is the accumulated movement cost from the starting zone to the current zone.

  * h(n) is the heuristic estimate of the remaining cost to the destination.

  * f(n) is the estimated total cost of a path through the current zone.

The current implementation uses Manhattan distance as its heuristic:

````text
h(n) = |xₙ - x_goal| + |yₙ - y_goal|
````

Movement costs depend on the destination zone's type:

| Zone type | Pathfinding cost | Meaning |
|----------------------------------------|
| normal    |       1.0        | Standard movement cost |
| priority  |       0.5        | Lower pathfinding cost |
| restricted|       2.0        | Higher pathfinding cost|
| blocked   |      infinite    | Zone cannot be entered |

The restricted cost should be made consistent in the implementation before the project is submitted. The intended simulation semantics are two turns for a restricted zone; the pathfinding cost is a separate concept.

### 3. Candidate route generation

The find_smart_paths() method repeatedly runs the pathfinding algorithm while applying penalties to intermediate zones used by previously discovered paths.

This encourages the algorithm to explore alternative routes instead of returning only the same shortest path.

The current implementation limits the search to ten iterations and increases penalties by 0.1 for each reused intermediate zone. The resulting paths are deduplicated, and calculate_turns() estimates the number of turns required for a given set of candidate routes.

These methods provide a heuristic approach to route selection; they do not guarantee a globally optimal solution.

### 4. Drone simulation and capacity management

The Simulation class assigns paths to drones and advances them through the graph.

Each drone maintains its assigned path and current position. Before moving, the simulation checks whether the next connection has available capacity and whether the destination zone can accept another drone.

Drones that cannot move must wait for a later turn.

The goal is to transport every drone to the destination while respecting the capacity constraints. The actual completion time depends on route lengths, shared connections, zone capacities, and the coordination of drone movements.

### 5. Graphical visualization

The project uses Pygame to display the graph and its current state.

The visualization includes:

* Zones: Drawn as circles at their map coordinates.

* Connections: Drawn as lines linking connected zones.

* Drones: Represented by small circles around the zones they occupy.

* Turn counter: Displays the current simulation turn.

* Step-by-step execution: Pressing the right arrow key advances the simulation.

The graphical interface helps users understand the graph topology, observe drone distribution, and follow the simulation one turn at a time.

## Resources

### Documentation and references

[Python Documentation](https://docs.python.org/3/)

[Python heapq Documentation](https://docs.python.org/3/library/heapq.html)

[Pygame Documentation](https://www.pygame.org/docs/)

[Explicación de A*](https://www.youtube.com/watch?v=hQa9JTtq4Ok)

[Tutorial de A*](https://www.datacamp.com/tutorial/a-star-algorithm)

[A* Search Algorithm — Red Blob Games](https://www.redblobgames.com/pathfinding/a-star/introduction.html)

[Graph Theory — NetworkX Documentation](https://networkx.org/documentation/stable/tutorial.html)

These resources were used as references for Python development, priority queues, graph representation, pathfinding concepts, and graphical rendering.

### AI usage

AI tools were used as a learning and development aid during the project.

Their use included:

* Explaining graph theory and pathfinding concepts, including A*.

* Reviewing algorithm design and discussing route selection strategies.

* Helping identify potential bugs and edge cases in Python code.

* Explaining Python classes, type hints, and interactions between modules.

* Assisting with the design and debugging of the Pygame visualization.

* Supporting the preparation of project documentation.

AI-generated suggestions were reviewed and adapted during development. The final implementation and understanding of the code remain the developer's responsibility.
