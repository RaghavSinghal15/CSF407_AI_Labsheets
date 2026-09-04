from collections import deque

WAREHOUSE = """#####################
#S....#............G#
#.##....##########..#
#....##.............#
#.######.###.#.###..#
#........#..........#
#####################"""


def bfs(text):
    grid = text.splitlines()
    start = next((r, c) for r, row in enumerate(grid) for c, cell in enumerate(row) if cell == 'S')
    goal = next((r, c) for r, row in enumerate(grid) for c, cell in enumerate(row) if cell == 'G')
    queue = deque([start])
    parent = {start: None}
    expanded = 0
    while queue:
        state = queue.popleft()
        if state == goal:
            path = []
            while state is not None:
                path.append(state)
                state = parent[state]
            return path[::-1], expanded
        expanded += 1
        r, c = state
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] != '#' and nxt not in parent:
                parent[nxt] = state
                queue.append(nxt)
    return None, expanded


if __name__ == '__main__':
    for name, grid in [('Warehouse', WAREHOUSE), ('Adjacent', '#####\n#SG##\n#####'),
                       ('Blocked', '#####\n#S#G#\n#####')]:
        path, expanded = bfs(grid)
        print(name)
        print('Path:', path if path is not None else 'No path found')
        print('Moves:', len(path) - 1 if path is not None else None)
        print('States expanded:', expanded)
