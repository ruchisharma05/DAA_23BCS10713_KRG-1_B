import pygame
import sys
import time
from collections import deque

pygame.init()

from ui import Button, draw_panel, THEME
from util import generate_random_maze
from algorithms import visualize_bfs, visualize_dijkstra, visualize_astar
ROWS = 25
COLS = 35
CELL_SIZE = 22
MARGIN = 2
PANEL_WIDTH = 220
FPS = 60

grid_width = COLS * (CELL_SIZE + MARGIN) + MARGIN
grid_height = ROWS * (CELL_SIZE + MARGIN) + MARGIN
width = grid_width + PANEL_WIDTH
height = grid_height + 100  # space for buttons

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Solver Dashboard")
clock = pygame.time.Clock()

# -------- GRID + STATE --------
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
start = (2, 2)
end = (ROWS - 3, COLS - 3)
grid[start[0]][start[1]] = 0
grid[end[0]][end[1]] = 0

stats = {"Algorithm": "None", "Visited": 0, "Path": 0}
visualization_running = False
# ------------------------------

# -------- BUTTONS -------------
# Panel and button layout
base_y = grid_height + 30  # position below the grid

btn_width_1 = 140
btn_width_2 = 170
total_button_width = (btn_width_1 * 4) + btn_width_2
total_gap = grid_width - total_button_width
gap = total_gap // 6 # 5 buttons, 6 gaps

x1 = gap
x2 = x1 + btn_width_1 + gap
x3 = x2 + btn_width_1 + gap
x4 = x3 + btn_width_1 + gap
x5 = x4 + btn_width_1 + gap

btn_bfs = Button("BFS", (x1, base_y), (btn_width_1, 40))
btn_dijkstra = Button("Dijkstra", (x2, base_y), (btn_width_1, 40))
btn_astar = Button("A*", (x3, base_y), (btn_width_1, 40))
btn_reset = Button("Reset Grid", (x4, base_y), (btn_width_1, 40))
btn_random = Button("Random Maze", (x5, base_y), (btn_width_2, 40))

buttons = [btn_bfs, btn_dijkstra, btn_astar, btn_reset, btn_random]
# ------------------------------


def draw_grid():
    """Draw the grid area."""
    # Draw grid background
    grid_bg_rect = pygame.Rect(0, 0, grid_width, grid_height)
    pygame.draw.rect(screen, THEME["grid_bg"], grid_bg_rect)
    
    for r in range(ROWS):
        for c in range(COLS):
            x = MARGIN + c * (CELL_SIZE + MARGIN)
            y = MARGIN + r * (CELL_SIZE + MARGIN)
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            color = THEME["grid"] # Default empty cell
            if (r, c) == start:
                color = THEME["start"]
            elif (r, c) == end:
                color = THEME["end"]
            elif grid[r][c] == 1:
                color = THEME["wall"]

            pygame.draw.rect(screen, color, rect, border_radius=3)

def clear_visualization():
    """Resets stats and redraws the grid to clear old paths."""
    stats["Visited"] = 0
    stats["Path"] = 0
    stats["Algorithm"] = "None"
    draw_grid() # Redraw the grid to clear path/visited nodes
    pygame.display.flip()


running = True

dragging_start = False
dragging_end = False
drawing_walls = False
erasing_walls = False


while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # --- Update hover states for buttons ---
    if not visualization_running:
        for b in buttons:
            b.check_hover(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Stop any drawing if visualization is running
        if visualization_running:
            continue
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = mouse_pos
            c = (mx - MARGIN) // (CELL_SIZE + MARGIN)
            r = (my - MARGIN) // (CELL_SIZE + MARGIN)

            # --- Check if click is inside grid ---
            if 0 <= r < ROWS and 0 <= c < COLS:
                if event.button == 1:  # left click
                    if (r, c) == start:
                        dragging_start = True
                    elif (r, c) == end:
                        dragging_end = True
                    elif grid[r][c] == 1:
                        erasing_walls = True
                        grid[r][c] = 0 # Erase first one
                    else:
                        drawing_walls = True
                        grid[r][c] = 1 # Draw first one
                        
                elif event.button == 3: # right click
                    # Clear wall to set start/end
                    grid[r][c] = 0 
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        start = (r, c)
                    else:
                        end = (r, c)
            
            # --- Check button clicks ---
            if btn_random.is_clicked(event):
                grid = generate_random_maze(ROWS, COLS, wall_prob=0.28, start=start, end=end)
                clear_visualization()

            elif btn_reset.is_clicked(event):
                grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                # Ensure start/end are clear
                grid[start[0]][start[1]] = 0
                grid[end[0]][end[1]] = 0
                clear_visualization()
                
            elif btn_bfs.is_clicked(event):
                clear_visualization()
                stats["Algorithm"] = "BFS"
                visualization_running = True
                visualize_bfs(screen, grid, start, end, CELL_SIZE, MARGIN, THEME, stats)
                visualization_running = False

            elif btn_dijkstra.is_clicked(event):
                clear_visualization()
                stats["Algorithm"] = "Dijkstra"
                visualization_running = True
                visualize_dijkstra(screen, grid, start, end, CELL_SIZE, MARGIN, THEME, stats)
                visualization_running = False

            elif btn_astar.is_clicked(event):
                clear_visualization()
                stats["Algorithm"] = "A*"
                visualization_running = True
                visualize_astar(screen, grid, start, end, CELL_SIZE, MARGIN, THEME, stats)
                visualization_running = False
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_start = False
                dragging_end = False
                drawing_walls = False
                erasing_walls = False
                
        elif event.type == pygame.MOUSEMOTION:
            mx, my = mouse_pos
            c = (mx - MARGIN) // (CELL_SIZE + MARGIN)
            r = (my - MARGIN) // (CELL_SIZE + MARGIN)
            
            if 0 <= r < ROWS and 0 <= c < COLS:
                # Drag start/end node
                if dragging_start and (r,c) != end and grid[r][c] == 0:
                    start = (r, c)
                elif dragging_end and (r,c) != start and grid[r][c] == 0:
                    end = (r, c)
                # Draw/Erase walls
                elif drawing_walls and (r,c) != start and (r,c) != end:
                    grid[r][c] = 1 # Draw
                elif erasing_walls and (r,c) != start and (r,c) != end:
                    grid[r][c] = 0 # Erase


    # --- Draw UI ---
    if not visualization_running:
        screen.fill(THEME["bg"])
        draw_grid()
        draw_panel(screen, stats, width, height, grid_width)

        # --- Draw buttons ---
        for b in buttons:
            b.draw(screen)

        pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()
sys.exit()