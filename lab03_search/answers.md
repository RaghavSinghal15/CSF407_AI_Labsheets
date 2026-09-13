# Search lab

Tasks 0 and 1

A state is the robot's (row, column) position in a non-wall cell. The map stays fixed, so no other changing information is needed in the state. Actions are up, down, left and right. A move goes to the adjacent cell if it is inside the map and not a wall.

The initial state is S at (1,1), the goal is G at (7,15), and every move costs 1. An action into a wall or outside the map is invalid. The problem is deterministic because a valid move has one definite result. A solution is a sequence of legal moves from S to G.

The map is stored as strings and positions as tuples. A* keeps a heap of candidates with their estimated total costs, their costs so far and their positions. A best-cost dictionary remembers the cheapest route found to each position, and parent links let the program reconstruct the final path. The program prints whether a solution was found, the path, its move count and the number of expanded states.

Tasks 2 and 3

The implementation is in `search.py`. On the original map it found a 40-move path and expanded 63 states. The adjacent-goal map gave one move and one expansion. The blocked-goal map gave no path after 9 expansions. On the alternative-path map it found a 6-move shortest route and expanded 13 states.

The code prints each path. It checks that the steps are adjacent, avoid walls and reach the goal. Comparing path length with BFS gives a separate check on whether the route is shortest for these unit-cost maps.

Task 4

The state is the coordinate tuple. `neighbours` generates valid actions and their successor positions. `state == goal` is the goal test. The variable g and the dictionary `costs` hold the cost from S. `heuristic` calculates h, the estimate of remaining cost. The heap priority is f = g + h, calculated using `new_g + heuristic(...)` for a new candidate.

The frontier is a heap, so A* takes the candidate with the lowest f first. A counter breaks ties in insertion order. A new route is added only if it improves the best known cost. An older heap entry is skipped if a better cost has already been found, so outdated candidates do not cause unnecessary work. `reconstruct` follows parent links back to S.

Here an expansion means generating a state's successors. The goal itself and outdated entries are not counted. If a better route causes a state to be expanded again, that is counted again.

Task 5

BFS and A* with Manhattan distance both found a solution of length 40 and both expanded 63 states. Neither expanded fewer states on this map. A* can save work when its estimate favours positions leading towards the goal, but a heuristic does not guarantee a saving on every map.

Task 6

With h = 0, A* found 40 moves and expanded 63 states. With Euclidean distance it also found 40 moves and expanded 63 states. With twice Manhattan distance it found 40 moves but expanded 66 states.

Manhattan distance adds the horizontal and vertical separation from the goal. Since only horizontal and vertical moves are allowed, this is the number of moves needed if walls are ignored. Walls cannot make the true route shorter, so Manhattan is a lower bound. It is also consistent: a single move changes it by at most the move cost of 1.

Euclidean distance is also a lower bound, but it usually gives less guidance for four-way movement. With h = 0, A* becomes uniform-cost search, which behaves like BFS here because all edges cost 1. Multiplying Manhattan by 2 can overestimate the remaining cost, so the shortest-path guarantee is lost. It happened to find the shortest length in this run; that does not make the weighted heuristic admissible.

Task 7

1. The frontier operations, valid-move checks and reconstruction worked on the checked maps. The output paths reached the intended goals.

2. No algorithm error was found in these runs. One detail worth checking was how outdated heap entries are handled after a better route is discovered.

3. Small maps with known answers, path replay and comparison with BFS were used to look for mistakes. The blocked map checked that failure terminates properly.

4. `heapq` provides the priority queue for A*, while `deque` gives the first-in-first-out queue for BFS. A stale entry is simply a candidate whose stored cost is no longer the best cost.

5. The final version uses best-cost updates, a fixed tie rule and stale-entry checks. These make its handling of repeated positions clear.

6. The no-solution map was useful for checking termination. The alternative-route map and BFS comparison were useful for checking shortest path length.

7. A plausible-looking path is not enough to trust the program. It could still cross a wall, use a diagonal step or reach the wrong cell, so the actual moves must be checked.

8. The comparison shows that informed search does not automatically mean fewer expansions. The result depends on how useful the heuristic is for the particular map.

Final reflection

1. Formulating the problem first fixes what a state, action, goal and cost mean. Otherwise a program might run correctly while solving a different navigation problem.

2. A* is informed because it uses h, an estimate of the distance still left, along with g, the cost already paid. BFS has no such estimate and explores by depth.

3. The heuristic changes the order of exploration and can affect optimality. A weak estimate gives little guidance; an overestimate may favour a longer path. The heuristic experiments showed the actual behaviour on this map.

4. The LLM helped translate the design into queue, heap and reconstruction code. Running small cases and comparing with BFS were still needed to check the implementation.

5. Accepting generated code without checking could hide wrong costs, invalid moves, repeated-state loops or a wrong goal test. Output that looks sensible does not establish that the algorithm is correct.
