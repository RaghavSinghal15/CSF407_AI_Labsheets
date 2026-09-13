# Search

## Tasks 0–1: Problem and design

States are non-wall (row, column) positions. Actions are up, down, left and right. A transition moves one cell if it is inside the grid and not blocked. The start is (1,1), the goal is (7,15), and each move costs 1.

Only the position changes because the map is fixed. An action into a wall or outside the grid is invalid. This is deterministic: each valid action has one result. A solution is a legal path from S to G.

The map is stored as strings. A* uses a heap frontier, best costs and parent links. The goal test compares the position with G. Parents reconstruct the path. The program reports success, path, move count and expanded states.

## Tasks 3–4: Checks and code

- Original map: path found, 40 moves, 63 expansions.
- Adjacent goal: path found, 1 move, 1 expansion.
- Blocked goal: no path, 9 expansions.
- Alternative paths: shortest path found, 6 moves, 13 expansions.

Paths are printed by the code and checked against BFS.

The coordinate tuple is the state. `neighbours` gives actions and transitions. `state == goal` is the goal test. `costs` stores g, `heuristic` calculates h, and `new_g + heuristic(...)` calculates f. The heap is the frontier and `reconstruct` follows parent links.

A* expands the state with lowest f = g + h. Equal priorities use insertion order. Best-cost checks prevent unnecessary repeats. Outdated heap entries are skipped, and a better route can reopen a state. Expansions count states whose successors are generated, excluding the goal.

## Tasks 5–6: Comparison

BFS and A* with Manhattan distance both found 40-move paths and expanded 63 states. A* did not save expansions on this map. A useful heuristic can guide it towards the goal, but this does not always reduce work.

All heuristic versions found a path:

- h = 0: 40 moves, 63 expansions.
- Euclidean distance: 40 moves, 63 expansions.
- Twice Manhattan distance: 40 moves, 66 expansions.

Manhattan distance is appropriate for horizontal and vertical moves. Ignoring walls gives a lower bound, so it is admissible and consistent. Euclidean distance is also a lower bound. With h = 0, A* becomes uniform-cost search, which acts like BFS here. Twice Manhattan can overestimate and does not guarantee the shortest path, even though this run still found 40 moves.

## Task 7

1. Queue/heap operations, valid moves and reconstruction worked in the checked runs.
2. No algorithm bug was found in these cases.
3. Known small maps, path checks and comparison with BFS were used to look for errors.
4. `heapq` selects by priority; `deque` gives a FIFO queue.
5. The final code uses best costs, fixed tie ordering and skips outdated entries.
6. The blocked case checked termination; BFS comparison checked shortest lengths.
7. The output should not be trusted without checking its moves and goal.
8. A* does not necessarily expand fewer states on every map.

## Final reflection

1. Specifying states, actions, goals and costs first makes the intended problem clear.
2. A* is informed because h estimates the remaining cost as well as using the cost already paid.
3. The heuristic changes search order and can affect optimality. Here twice Manhattan caused more expansions.
4. The LLM helped translate the design into heap, queue and path-reconstruction code.
5. Unchecked generated code could use illegal moves, wrong costs or a wrong goal, or fail to terminate.
