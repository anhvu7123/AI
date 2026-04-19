import heapq
import math

def reconstruct_path(came_from, goal):
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path


def astar_graph(graph, start, goal, heuristic):
    def h(node):
        if callable(heuristic):
            return heuristic(node, goal)
        return heuristic.get(node, 0)

    open_heap = []
    heapq.heappush(open_heap, (h(start), 0, start))

    came_from = {start: None}
    g_score = {start: 0}
    closed = set()

    while open_heap:
        f, g, current = heapq.heappop(open_heap)

        if current in closed:
            continue

        if current == goal:
            path = reconstruct_path(came_from, goal)
            return path, g_score[goal]

        closed.add(current)

        for neighbor, cost in graph[current].items():
            tentative_g = g + cost

            if neighbor in closed and tentative_g >= g_score.get(neighbor, math.inf):
                continue

            if tentative_g < g_score.get(neighbor, math.inf):
                g_score[neighbor] = tentative_g
                came_from[neighbor] = current
                heapq.heappush(open_heap, (tentative_g + h(neighbor), tentative_g, neighbor))

    return None, math.inf


def main():
    print("=== BAI III.2: A* tim duong tren do thi ===")

    graph = {
        'A': {'B': 4, 'C': 3},
        'B': {'A': 4, 'D': 5, 'E': 12},
        'C': {'A': 3, 'D': 7, 'F': 10},
        'D': {'B': 5, 'C': 7, 'E': 2, 'F': 2},
        'E': {'B': 12, 'D': 2, 'G': 5},
        'F': {'C': 10, 'D': 2, 'G': 3},
        'G': {'E': 5, 'F': 3}
    }

    coords = {
        'A': (0, 0),
        'B': (2, 2),
        'C': (2, -1),
        'D': (5, 1),
        'E': (8, 2),
        'F': (7, -1),
        'G': (10, 0)
    }

    def heuristic(node, goal):
        x1, y1 = coords[node]
        x2, y2 = coords[goal]
        return abs(x1 - x2) + abs(y1 - y2)

    start = 'A'
    goal = 'G'

    path, cost = astar_graph(graph, start, goal, heuristic)

    print(f"Duong di tu {start} den {goal}: {path}")
    print("Tong chi phi:", cost)


if __name__ == "__main__":
    main()