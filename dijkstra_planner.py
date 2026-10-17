import heapq
import numpy as np
import matplotlib.pyplot as plt

# Grid map: 0 = free, 1 = obstacle
grid = np.zeros((15, 15), dtype=int)
grid[3, 2:10] = 1
grid[3:9, 9] = 1
grid[8, 4:14] = 1
grid[11:14, 6] = 1

start = (1, 1)
goal = (13, 13)


def dijkstra(grid, start, goal):
    queue = [(0, start)]          # (distance so far, cell)
    dist = {start: 0}
    parent = {start: None}
    explored = []

    while queue:
        d, cell = heapq.heappop(queue)
        if cell in explored:
            continue
        explored.append(cell)

        if cell == goal:          # done: walk back through parents
            path = []
            while cell is not None:
                path.append(cell)
                cell = parent[cell]
            return path[::-1], explored

        r, c = cell
        for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if 0 <= nr < 15 and 0 <= nc < 15 and grid[nr, nc] == 0:
                if d + 1 < dist.get((nr, nc), 999):
                    dist[(nr, nc)] = d + 1
                    parent[(nr, nc)] = cell
                    heapq.heappush(queue, (d + 1, (nr, nc)))
    return None, explored


path, explored = dijkstra(grid, start, goal)
print("Explored cells:", len(explored))
print("Path length:", len(path) - 1)

# Plot
plt.imshow(grid, cmap="gray_r")                      # white = free, black = obstacle
ey, ex = zip(*explored)
plt.scatter(ex, ey, c="lightblue", marker="s", s=250, label="Explored")
py, px = zip(*path)
plt.plot(px, py, "r-", linewidth=3, label="Final path")
plt.scatter(start[1], start[0], c="green", s=150, label="Start")
plt.scatter(goal[1], goal[0], c="gold", s=300, marker="*", label="Goal")
plt.imshow(grid, cmap="gray_r", alpha=(grid == 1).astype(float))   # draw obstacles on top
plt.title("Dijkstra path planning (black = obstacle, white = free)")
plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=4)
plt.savefig("dijkstra_result.png", bbox_inches="tight")
plt.show()
