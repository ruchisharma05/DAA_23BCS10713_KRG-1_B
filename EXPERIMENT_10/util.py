import random

def generate_random_maze(rows, cols, wall_prob=0.25, start=None, end=None):
    """
    Generates a random maze grid.
    - 0 = empty cell
    - 1 = wall
    wall_prob = probability that a cell becomes a wall
    """
    grid = [[0 if random.random() > wall_prob else 1 for _ in range(cols)] for _ in range(rows)]

    if start:
        grid[start[0]][start[1]] = 0
    if end:
        grid[end[0]][end[1]] = 0

    return grid