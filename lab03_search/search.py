"""Four-neighbour grid search; run this file to reproduce the lab experiments."""
from collections import deque
from heapq import heappop, heappush
from itertools import count
from math import hypot

WAREHOUSE = """#################
#S....#.........#
#.###.#.#######.#
#...#.#.......#.#
###.#.#######.#.#
#...#.........#.#
#.###########.#.#
#.............#G#
#################"""


def parse_grid(text):
    rows = text.strip().splitlines()
    if not rows or any(set(row) - set('#.SG') for row in rows):
        raise ValueError('Invalid grid symbols')
    if len(set(map(len, rows))) != 1:
        raise ValueError('Grid rows must have equal lengths')
    grid = rows
    starts = [(r, c) for r, row in enumerate(grid) for c, x in enumerate(row) if x == 'S']
    goals = [(r, c) for r, row in enumerate(grid) for c, x in enumerate(row) if x == 'G']
    if len(starts) != 1 or len(goals) != 1:
        raise ValueError('Exactly one S and one G required')
    return grid, starts[0], goals[0]


def neighbours(grid, state):
    r, c = state
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] != '#':
            yield nr, nc


def reconstruct(parent, goal):
    path = [goal]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return path[::-1]


def heuristic(state, goal, mode):
    dr, dc = abs(state[0] - goal[0]), abs(state[1] - goal[1])
    return {'zero': 0, 'manhattan': dr + dc,
            'euclidean': hypot(dr, dc), 'weighted': 2 * (dr + dc)}[mode]


def search(text, algorithm='astar', mode='manhattan'):
    grid, start, goal = parse_grid(text)
    parent, costs, expanded = {start: None}, {start: 0}, 0
    if algorithm == 'bfs':
        frontier = deque([start])
        while frontier:
            state = frontier.popleft()
            if state == goal:
                return result(reconstruct(parent, goal), expanded)
            expanded += 1
            for nxt in neighbours(grid, state):
                if nxt not in parent:
                    parent[nxt] = state
                    frontier.append(nxt)
    elif algorithm == 'astar':
        serial = count()
        frontier = [(heuristic(start, goal, mode), next(serial), 0, start)]
        while frontier:
            _, _, g, state = heappop(frontier)
            if g != costs[state]:
                continue
            if state == goal:
                return result(reconstruct(parent, goal), expanded)
            expanded += 1
            for nxt in neighbours(grid, state):
                new_g = g + 1
                if new_g < costs.get(nxt, float('inf')):
                    costs[nxt], parent[nxt] = new_g, state
                    heappush(frontier, (new_g + heuristic(nxt, goal, mode),
                                        next(serial), new_g, nxt))
    else:
        raise ValueError('Use bfs or astar')
    return result(None, expanded)


def result(path, expanded):
    return {'found': path is not None, 'path': path,
            'length': len(path) - 1 if path is not None else None, 'expanded': expanded}


def valid_path(text, path):
    grid, start, goal = parse_grid(text)
    return bool(path) and path[0] == start and path[-1] == goal and all(
        b in list(neighbours(grid, a)) for a, b in zip(path, path[1:]))


def draw_path(text, path):
    grid, _, _ = parse_grid(text)
    grid = [list(row) for row in grid]
    for r, c in (path or [])[1:-1]:
        grid[r][c] = '*'
    return '\n'.join(''.join(row) for row in grid)


def experiments():
    maps = {'original': WAREHOUSE, 'adjacent': '#####\n#SG##\n#####',
            'blocked': '#######\n#S....#\n###.###\n#...#G#\n#######',
            'alternatives': '#######\n#S....#\n#..#..#\n#....G#\n#######'}
    tests = {name: search(text) for name, text in maps.items()}
    for name, value in tests.items():
        if value['found']:
            assert valid_path(maps[name], value['path'])
            assert value['length'] == search(maps[name], 'bfs')['length']
    assert tests['adjacent']['length'] == 1 and not tests['blocked']['found']
    comparisons = {'bfs': search(WAREHOUSE, 'bfs')}
    comparisons.update({mode: search(WAREHOUSE, mode=mode)
                        for mode in ['manhattan', 'zero', 'euclidean', 'weighted']})
    return {'tests': tests, 'comparisons': comparisons,
            'expansion_definition': 'Non-goal states whose successors are generated; stale heap entries excluded.'}


if __name__ == '__main__':
    output = experiments()
    for name, value in output['tests'].items():
        print(name, 'found:', value['found'], 'moves:', value['length'], 'expanded:', value['expanded'])
        print('Path:', value['path'])
    print('\nBFS and heuristic comparison')
    for name, value in output['comparisons'].items():
        print(name, 'found:', value['found'], 'moves:', value['length'], 'expanded:', value['expanded'])
    print(draw_path(WAREHOUSE, output['tests']['original']['path']))
