import pygame
import random
import time

# Constants
CELL_WIDTH = 20
CELL_HEIGHT = 7
MAZE_WIDTH = CELL_WIDTH * 2 + 1
MAZE_HEIGHT = CELL_HEIGHT * 2 + 1

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

def show_popup(screen, message, font, image_size):
    overlay = pygame.Surface(image_size)
    overlay.set_alpha(180)
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, 0))

    text = font.render(message, True, (0, 0, 0))
    rect = text.get_rect(center=(image_size[0] // 2, image_size[1] // 2))
    screen.blit(text, rect)
    pygame.display.flip()
    time.sleep(2)

