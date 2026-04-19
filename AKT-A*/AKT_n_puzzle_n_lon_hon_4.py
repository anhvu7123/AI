import heapq

class NPuzzleAKT:
    def __init__(self, n):
        self.n = n
        self.goal = tuple(list(range(1, n * n)) + [0])
        self.goal_pos = {}
        for idx, value in enumerate(self.goal):
            self.goal_pos[value] = (idx // n, idx % n)

    def print_state(self, state):
        for i in range(self.n):
            row = state[i * self.n:(i + 1) * self.n]
            print(" ".join(f"{x:2}" if x != 0 else " ." for x in row))
        print()

    def manhattan(self, state):
        dist = 0
        for idx, value in enumerate(state):
            if value == 0:
                continue
            r, c = idx // self.n, idx % self.n
            gr, gc = self.goal_pos[value]
            dist += abs(r - gr) + abs(c - gc)
        return dist

    def is_goal(self, state):
        return state == self.goal

    def get_neighbors(self, state):
        n = self.n
        zero_idx = state.index(0)
        zr, zc = zero_idx // n, zero_idx % n

        directions = [
            (-1, 0, "UP"),
            (1, 0, "DOWN"),
            (0, -1, "LEFT"),
            (0, 1, "RIGHT")
        ]

        neighbors = []
        for dr, dc, action in directions:
            nr, nc = zr + dr, zc + dc
            if 0 <= nr < n and 0 <= nc < n:
                ni = nr * n + nc
                new_state = list(state)
                new_state[zero_idx], new_state[ni] = new_state[ni], new_state[zero_idx]
                neighbors.append((tuple(new_state), action))
        return neighbors

    def inversion_count(self, state):
        arr = [x for x in state if x != 0]
        inv = 0
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    inv += 1
        return inv

    def is_solvable(self, state):
        inv = self.inversion_count(state)

        if self.n % 2 == 1:
            return inv % 2 == 0
        else:
            zero_row_from_top = state.index(0) // self.n
            zero_row_from_bottom = self.n - zero_row_from_top
            return (zero_row_from_bottom % 2 == 0 and inv % 2 == 1) or \
                   (zero_row_from_bottom % 2 == 1 and inv % 2 == 0)

    def solve(self, start):
        start = tuple(start)

        if not self.is_solvable(start):
            return None, None, None

        open_heap = []
        g_score = {start: 0}
        parent = {start: None}
        move_taken = {start: None}
        closed = set()
        counter = 0

        h0 = self.manhattan(start)
        heapq.heappush(open_heap, (h0, 0, counter, start))

        expanded = 0

        while open_heap:
            f, g, _, current = heapq.heappop(open_heap)

            if current in closed:
                continue

            closed.add(current)
            expanded += 1

            if self.is_goal(current):
                path = []
                moves = []

                node = current
                while node is not None:
                    path.append(node)
                    if move_taken[node] is not None:
                        moves.append(move_taken[node])
                    node = parent[node]

                path.reverse()
                moves.reverse()
                return path, moves, expanded

            for neighbor, action in self.get_neighbors(current):
                if neighbor in closed:
                    continue

                tentative_g = g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    parent[neighbor] = current
                    move_taken[neighbor] = action
                    counter += 1
                    h = self.manhattan(neighbor)
                    heapq.heappush(open_heap, (tentative_g + h, tentative_g, counter, neighbor))

        return None, None, expanded


def main():
    print("=== BAI IV.1: AKT cho N-puzzle (n>4) ===")

    n = 5
    puzzle = NPuzzleAKT(n)

    start = (
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 23, 0, 24
    )

    print(f"Trang thai bat dau {n}x{n}:")
    puzzle.print_state(start)

    path, moves, expanded = puzzle.solve(start)

    if path is None:
        print("Khong giai duoc.")
        return

    print("So buoc:", len(moves))
    print("So nut da mo rong:", expanded)
    print("Chuoi di chuyen:", moves)

    print("\nCac trang thai:")
    for state in path:
        puzzle.print_state(state)


if __name__ == "__main__":
    main()