# Agents lab

Task 1

1. The environment is the warehouse grid. The # cells are shelves or obstacles, and the other cells are places the vehicle can enter.

2. The goal is to reach G from S without going through an obstacle. The route should consist of valid grid moves.

3. The vehicle can move up, down, left or right. Each action changes its position by one cell; diagonal moves are not allowed.

4. It needs its current position, the warehouse map and the goal position. For BFS it also keeps a queue of positions to explore, the positions already discovered and a parent for each position so the route can be recovered.

5. This is a goal-based agent because it chooses a sequence of actions to reach a specified destination. A simple reflex rule would only react to the current situation without planning the full route.

If the warehouse becomes larger, BFS still works, but it may need much more time and memory. If both dimensions double, there can be about four times as many cells. A* could help guide the search on a larger map. Moving obstacles would also require the map and plan to be updated.

Task 2

The map is stored as a list of strings, and a state is a (row, column) position. The agent tries the four neighbouring cells and rejects any that are outside the map or blocked. BFS explores positions in order of distance from S until it reaches G.

The queue is the set of positions waiting to be explored. Each newly discovered position stores where it came from. Starting at G and following those parents back to S gives the path in reverse, which is then reversed for printing.

BFS is suitable here because every move has the same cost. It finds a path with the fewest moves and avoids loops by marking positions when they enter the queue.

Task 3 and results

The final program ran successfully on the given warehouse and the two small checks. The given warehouse had a 20-move path, with 58 states expanded. With G next to S, it found the expected one-move path and expanded one state. With the goal blocked, it reported no path and expanded one state. The actual paths are printed by `agent.py`.

BFS was used because the map is small, finite and has equal move costs. A clear specification of the map symbols, allowed moves and expected output is more useful than simply asking for a robot program. If a generated version fails, including the map, error message and expected behaviour makes the correction request easier to act on.

The LLM helped turn the design into BFS and path-reconstruction code. The program ran without errors on the three checked maps. The important checks are that every step is legal, the last position is G, and an unreachable goal causes failure rather than an endless search.
