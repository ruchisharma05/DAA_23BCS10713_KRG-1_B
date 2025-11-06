import pygame
import time
import heapq
import sys
from collections import deque

def draw_path(screen, parent, start, end, cell_size, margin, theme, stats):
    path = []
    cell = end
    while cell in parent:
        path.append(cell)
        cell = parent[cell]
    path.reverse()
    stats["Path"] = len(path)

    for (r, c) in path:
        if (r, c) != start and (r, c) != end:
            x_pos = margin + c * (cell_size + margin)
            y_pos = margin + r * (cell_size + margin)
            rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, theme["path"], rect, border_radius=4)
            pygame.display.update(rect)
            time.sleep(0.015)
            
    pygame.time.wait(2000)


def visualize_bfs(screen, grid, start, end, cell_size, margin, theme, stats):
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    visited = set([start])
    parent = {}
    stats["Visited"] = 0
    stats["Path"] = 0

    while queue:
        for event in pygame.event.get(pygame.QUIT):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        r, c = queue.popleft()
        stats["Visited"] = len(visited)

        if (r, c) != start and (r, c) != end:
            x_pos = margin + c * (cell_size + margin)
            y_pos = margin + r * (cell_size + margin)
            rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, theme["visited"], rect, border_radius=4)
            pygame.display.update(rect)
            time.sleep(0.005)

        if (r, c) == end:
            draw_path(screen, parent, start, end, cell_size, margin, theme, stats)
            return

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))
    return


def visualize_dijkstra(screen, grid, start, end, cell_size, margin, theme, stats):
    rows, cols = len(grid), len(grid[0])
    pq = [(0, start)]
    cost = {start: 0}
    parent = {}
    visited = set()
    stats["Visited"] = 0
    stats["Path"] = 0

    while pq:
        for event in pygame.event.get(pygame.QUIT):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_cost, (r, c) = heapq.heappop(pq)
        if (r, c) in visited:
            continue
        visited.add((r, c))
        stats["Visited"] = len(visited)

        if (r, c) != start and (r, c) != end:
            x_pos = margin + c * (cell_size + margin)
            y_pos = margin + r * (cell_size + margin)
            rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, theme["visited"], rect, border_radius=4)
            pygame.display.update(rect)
            time.sleep(0.005)

        if (r, c) == end:
            draw_path(screen, parent, start, end, cell_size, margin, theme, stats)
            return

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                new_cost = current_cost + 1
                if (nr, nc) not in cost or new_cost < cost[(nr, nc)]:
                    cost[(nr, nc)] = new_cost
                    parent[(nr, nc)] = (r, c)
                    heapq.heappush(pq, (new_cost, (nr, nc)))
    return


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def visualize_astar(screen, grid, start, end, cell_size, margin, theme, stats):
    rows, cols = len(grid), len(grid[0])
    pq = [(0, start)]
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    parent = {}
    open_set_hash = {start}
    stats["Visited"] = 0
    stats["Path"] = 0

    while pq:
        for event in pygame.event.get(pygame.QUIT):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        _, current = heapq.heappop(pq)
        r, c = current
        if current not in open_set_hash:
            continue
        open_set_hash.remove(current)
        stats["Visited"] += 1

        if current == end:
            draw_path(screen, parent, start, end, cell_size, margin, theme, stats)
            return

        if (r, c) != start:
            x_pos = margin + c * (cell_size + margin)
            y_pos = margin + r * (cell_size + margin)
            rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, theme["visited"], rect, border_radius=4)
            pygame.display.update(rect)
            time.sleep(0.005)

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    parent[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                    if neighbor not in open_set_hash:
                        heapq.heappush(pq, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
                        if neighbor != end:
                            x_pos = margin + nc * (cell_size + margin)
                            y_pos = margin + nr * (cell_size + margin)
                            rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
                            pygame.draw.rect(screen, theme["frontier"], rect, border_radius=4)
                            pygame.display.update(rect)
    return
