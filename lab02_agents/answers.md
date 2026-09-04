# Agents

## Task 1

1. The environment is the warehouse grid. Shelves are blocked cells.
2. The goal is to move from S to G without hitting a shelf.
3. Actions are up, down, left and right, one cell at a time.
4. The agent needs its current position, map and goal. It also stores the search frontier, visited positions and parents.
5. It is goal-based because it plans a route to a destination instead of reacting only to its current surroundings.

## Task 2: Design

The map is a list of strings and the state is a (row, column) tuple. Valid moves stay inside the grid and avoid walls. BFS uses the map, current state and goal to find the next actions. Parent links are used to reconstruct the path.

All moves cost one, so BFS finds a shortest path. Positions are marked visited when added to the queue to avoid repeats.

## Results

The supplied warehouse needed 20 moves and expanded 58 states. The adjacent goal needed 1 move and expanded 1 state. The blocked goal had no solution and expanded 1 state. The program prints the paths.

BFS is suitable for this small static grid. A larger warehouse needs more time and memory. Doubling both dimensions gives roughly four times as many cells. A* could reduce the search, and moving obstacles would need replanning.

## Reflection

The LLM helped implement BFS and path reconstruction. The original map, adjacent goal and blocked goal were checked. A plausible route alone is not enough: every step must be valid and the route must end at G. If a program fails, the map, error and expected result help describe the problem clearly.
