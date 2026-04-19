import heapq
import math
from functools import lru_cache

class DeliveryAStar:
    def __init__(self, grid):
        self.grid = [list(row) for row in grid]
        self.R = len(grid)
        self.C = len(grid[0]) if self.R > 0 else 0

        self.start = None
        self.goal = None
        self.deliveries = []

        for r in range(self.R):
            for c in range(self.C):
                if self.grid[r][c] == 'S':
                    self.start = (r, c)
                elif self.grid[r][c] == 'G':
                    self.goal = (r, c)
                elif self.grid[r][c] == 'D':
                    self.deliveries.append((r, c))

        if self.start is None or self.goal is None:
            raise ValueError("Grid phai co S va G.")

        self.delivery_index = {pos: i for i, pos in enumerate(self.deliveries)}
        self.full_mask = (1 << len(self.deliveries)) - 1

    def inside(self, r, c):
        return 0 <= r < self.R and 0 <= c < self.C

    def passable(self, r, c):
        return self.grid[r][c] != '#'

    def neighbors(self, r, c):
        for dr, dc, action in [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]:
            nr, nc = r + dr, c + dc
            if self.inside(nr, nc) and self.passable(nr, nc):
                yield nr, nc, action

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @lru_cache(maxsize=None)
    def mst_cost(self, points_tuple):
        points = list(points_tuple)
        if len(points) <= 1:
            return 0

        used = {points[0]}
        total = 0

        while len(used) < len(points):
            best = math.inf
            best_point = None
            for u in used:
                for v in points:
                    if v not in used:
                        w = self.manhattan(u, v)
                        if w < best:
                            best = w
                            best_point = v
            used.add(best_point)
            total += best

        return total

    def heuristic(self, pos, mask):
        remaining = []
        for i, d in enumerate(self.deliveries):
            if not (mask & (1 << i)):
                remaining.append(d)

        if not remaining:
            return self.manhattan(pos, self.goal)

        points = remaining + [self.goal]
        nearest = min(self.manhattan(pos, p) for p in points)
        mst = self.mst_cost(tuple(sorted(points)))
        return nearest + mst

    def solve(self):
        start_state = (self.start[0], self.start[1], 0)

        open_heap = []
        heapq.heappush(open_heap, (self.heuristic(self.start, 0), 0, start_state))

        g_score = {start_state: 0}
        parent = {start_state: None}
        action_taken = {start_state: None}
        closed = set()

        while open_heap:
            f, g, state = heapq.heappop(open_heap)

            if state in closed:
                continue
            closed.add(state)

            r, c, mask = state

            if (r, c) == self.goal and mask == self.full_mask:
                path = []
                actions = []

                node = state
                while node is not None:
                    path.append(node)
                    if action_taken[node] is not None:
                        actions.append(action_taken[node])
                    node = parent[node]

                path.reverse()
                actions.reverse()
                return path, actions, g

            for nr, nc, action in self.neighbors(r, c):
                new_mask = mask
                if (nr, nc) in self.delivery_index:
                    bit = self.delivery_index[(nr, nc)]
                    new_mask |= (1 << bit)

                next_state = (nr, nc, new_mask)
                tentative_g = g + 1

                if next_state in closed and tentative_g >= g_score.get(next_state, math.inf):
                    continue

                if tentative_g < g_score.get(next_state, math.inf):
                    g_score[next_state] = tentative_g
                    parent[next_state] = state
                    action_taken[next_state] = action
                    h = self.heuristic((nr, nc), new_mask)
                    heapq.heappush(open_heap, (tentative_g + h, tentative_g, next_state))

        return None, None, math.inf

    def print_grid(self):
        for row in self.grid:
            print(" ".join(row))
        print()

    def draw_path(self, path):
        board = [row[:] for row in self.grid]
        for r, c, mask in path:
            if board[r][c] == '.':
                board[r][c] = '*'
        for row in board:
            print(" ".join(row))
        print()


def main():
    print("=== BAI IV.2: Bai toan nguoi giao hang theo A* ===")

    grid = [
        "S..#....",
        ".#..D#..",
        "...#....",
        "..D...#.",
        ".##.....",
        "....#D.G"
    ]

    solver = DeliveryAStar(grid)

    print("Ban do:")
    solver.print_grid()

    path, actions, cost = solver.solve()

    if path is None:
        print("Khong tim duoc lo trinh giao hang.")
        return

    print("Tong chi phi:", cost)
    print("Chuoi hanh dong:", actions)
    print("So buoc:", len(actions))

    print("\nDuong di danh dau bang '*':")
    solver.draw_path(path)


if __name__ == "__main__":
    main()