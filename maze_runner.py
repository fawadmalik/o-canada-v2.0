import pygame
import sys
import random
import time
from maze_lib import show_popup  # Add this at the top of your file

# Constants
CELL_WIDTH = 18
CELL_HEIGHT = 5
MAZE_WIDTH = CELL_WIDTH * 2 + 1
MAZE_HEIGHT = CELL_HEIGHT * 2 + 1
MAX_TIME = 30
NUM_PREGENERATED_MAZES = 2
MAX_ATTEMPTS = 2  # After 2 failed mazes, game ends

# Game state variables (made global)
maze_pool = []
current_maze_index = 0
raw_grid = None
ascii_maze = None
player_pos = [1, 1]
exit_pos = [MAZE_WIDTH - 2, MAZE_HEIGHT - 2]
start_time = 0

def generate_maze_grid():
    grid = [["█" if x % 2 == 0 or y % 2 == 0 else " " for x in range(MAZE_WIDTH)] for y in range(MAZE_HEIGHT)]
    visited = [[False for _ in range(CELL_WIDTH)] for _ in range(CELL_HEIGHT)]

    def carve(x, y):
        dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        random.shuffle(dirs)
        visited[y][x] = True
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < CELL_WIDTH and 0 <= ny < CELL_HEIGHT and not visited[ny][nx]:
                grid[y * 2 + 1 + dy][x * 2 + 1 + dx] = " "
                grid[ny * 2 + 1][nx * 2 + 1] = " "
                carve(nx, ny)

    grid[1][1] = " "
    grid[0][1] = " "
    grid[MAZE_HEIGHT - 1][MAZE_WIDTH - 2] = " "
    carve(0, 0)
    return grid

def to_box_drawing(grid):
    def get_char(x, y):
        if grid[y][x] != "█":
            return " "
        up = y > 0 and grid[y - 1][x] == "█"
        down = y < len(grid) - 1 and grid[y + 1][x] == "█"
        left = x > 0 and grid[y][x - 1] == "█"
        right = x < len(grid[0]) - 1 and grid[y][x + 1] == "█"
        if up and down and left and right: return "┼"
        if up and down and left: return "┤"
        if up and down and right: return "├"
        if left and right and up: return "┴"
        if left and right and down: return "┬"
        if up and down: return "│"
        if left and right: return "─"
        if down and right: return "┌"
        if down and left: return "┐"
        if up and right: return "└"
        if up and left: return "┘"
        if up or down: return "│"
        if left or right: return "─"
        return "•"
    return ["".join(get_char(x, y) for x in range(len(grid[0]))) for y in range(len(grid))]

def is_walkable(grid, x, y):
    return 0 <= x < MAZE_WIDTH and 0 <= y < MAZE_HEIGHT and grid[y][x] == " "

def preload_mazes(n):
    return [generate_maze_grid() for _ in range(n)]

def reset_maze():
    global current_maze_index, raw_grid, ascii_maze, player_pos, start_time
    current_maze_index = (current_maze_index + 1) % NUM_PREGENERATED_MAZES
    raw_grid = maze_pool[current_maze_index]
    ascii_maze = to_box_drawing(raw_grid)
    player_pos[:] = [1, 1]
    start_time = time.time()

# --- Main body

pygame.init()

# Load mazes
maze_pool = preload_mazes(NUM_PREGENERATED_MAZES)
raw_grid = maze_pool[current_maze_index]
ascii_maze = to_box_drawing(raw_grid)

# Load background
bg_image = pygame.image.load("images/Maze of Madness.png")
image_width, image_height = bg_image.get_size()

# Fonts and layout
font_size = int(min(image_width * 0.8 // MAZE_WIDTH, image_height * 0.8 // MAZE_HEIGHT))
font = pygame.font.SysFont("Courier New", font_size, bold=True)
arrow_font = pygame.font.SysFont("Segoe UI Symbol", font_size + 4, bold=True)
offset_x = (image_width - MAZE_WIDTH * font_size) // 2
offset_y = (image_height - MAZE_HEIGHT * font_size) // 2

screen = pygame.display.set_mode((image_width, image_height))
pygame.display.set_caption("Timed Maze Adventure")
clock = pygame.time.Clock()

start_time = time.time()
running = True

while running:
    screen.blit(bg_image, (0, 0))

    # Timer logic
    elapsed = time.time() - start_time
    remaining = max(0, int(MAX_TIME - elapsed))
    if remaining == 0:
        reset_maze()

    # Draw maze
    for y, row in enumerate(ascii_maze):
        for x, char in enumerate(row):
            screen_x = offset_x + x * font_size
            screen_y = offset_y + y * font_size

            if [x, y] == player_pos:
                color = (0, 255, 0)
                char = "●"
            elif [x, y] == exit_pos:
                color = (255, 0, 0)
                char = "■"
            elif raw_grid[y][x] == "█":
                color = (0, 0, 0)
            else:
                color = (0, 0, 0)

            text = font.render(char, True, color)
            screen.blit(text, (screen_x, screen_y))

    # Arrows
    entry_arrow = arrow_font.render("⮕", True, (0, 0, 0))
    screen.blit(entry_arrow, (offset_x + font_size, offset_y - font_size))
    exit_arrow = arrow_font.render("⮔", True, (0, 0, 0))
    screen.blit(exit_arrow, (offset_x + (MAZE_WIDTH - 2) * font_size, offset_y + MAZE_HEIGHT * font_size))

    # Timer
    timer_text = font.render(f"Time: {remaining}s", True, (0, 0, 0))
    screen.blit(timer_text, (20, 20))

    pygame.display.flip()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    x, y = player_pos
    if keys[pygame.K_UP] and is_walkable(raw_grid, x, y - 1): y -= 1
    if keys[pygame.K_DOWN] and is_walkable(raw_grid, x, y + 1): y += 1
    if keys[pygame.K_LEFT] and is_walkable(raw_grid, x - 1, y): x -= 1
    if keys[pygame.K_RIGHT] and is_walkable(raw_grid, x + 1, y): x += 1
    player_pos = [x, y]

    if player_pos == exit_pos:
        show_popup(screen, "You escaped the maze!", font, (image_width/2, image_height/2))
        running = False

    clock.tick(10)

pygame.quit()
sys.exit()
