import pygame
import sys
import json
from mylib import reset, visitedall, prov
from character import Character

# Load data from JSON file
with open("rooms.json", "r") as file:
    data = json.load(file)

# Accessing the dictionaries
east = data["east"]
west = data["west"]
north = data["north"]
south = data["south"]
visited = data["visited"]

game_end_locations = ["hell"]
image_and_caption = {"current_image": "", "current_caption": ""}

# Define colours
black = (0, 0, 0)
white = (255, 255, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("O Canada!")
font = pygame.font.SysFont(None, 36)

# -------------------
# Game Setup
# -------------------

# Start in the first room (top left of the map)
where = list(north.keys())[0]
prov(where, visited, image_and_caption)

# Create player character
player = Character(role="PC", color=(255, 0, 0))
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# -------------------
# Main Game Loop
# -------------------
clock = pygame.time.Clock()  # Add a clock for consistent frame rate

running = True
game_over = False  # Track if the game is in "hell" state

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Global reset (r) and quit (q) keys
            if event.key == pygame.K_r:
                where = reset(where, visited, image_and_caption)
                player.move_to_center()
                game_over = False
            elif event.key == pygame.K_q:
                running = False

    # Only process movement if not in "hell"
    if where not in game_end_locations and not game_over:
        keys = pygame.key.get_pressed()
        player.direction = pygame.Vector2(0, 0)

        # Horizontal movement (independent checks for left/right)
        if keys[pygame.K_LEFT]:
            player.direction.x = -1
        if keys[pygame.K_RIGHT]:
            player.direction.x = 1

        # Vertical movement (independent checks for up/down)
        if keys[pygame.K_UP]:
            player.direction.y = -1
        if keys[pygame.K_DOWN]:
            player.direction.y = 1

        # Normalize diagonal movement to avoid faster speed
        if player.direction.length() > 0:
            player.direction = player.direction.normalize()

        # Update sprite positions
        all_sprites.update()

        # -------------------
        # Room Boundary Logic
        # -------------------

        # Room image bounds
        left_bound = 200
        right_bound = 600
        top_bound = 100
        bottom_bound = 340

        if player.rect.left < left_bound:
            next_room = west[where]
            where = next_room
            prov(where, visited, image_and_caption)
            if where in game_end_locations:
                game_over = True
                player.move_to_center()
            else:
                player.move_to_edge("right")


        elif player.rect.right > right_bound:
            next_room = east[where]
            where = next_room
            prov(where, visited, image_and_caption)
            if where in game_end_locations:
                game_over = True
                player.move_to_center()
            else:
                player.move_to_edge("left")

        elif player.rect.top < top_bound:
            next_room = north[where]
            where = next_room
            prov(where, visited, image_and_caption)
            if where in game_end_locations:
                game_over = True
                player.move_to_center()
            else:
                player.move_to_edge("down")

        elif player.rect.bottom > bottom_bound:
            next_room = south[where]
            where = next_room
            prov(where, visited, image_and_caption)
            if where in game_end_locations:
                game_over = True
                player.move_to_center()
            else:
                player.move_to_edge("up")

    # -------------------
    # Drawing
    # -------------------
    screen.fill(white)
    screen.blit(image_and_caption["current_image"], (200, 100))
    caption_text = font.render(image_and_caption["current_caption"], True, black)
    screen.blit(caption_text, (300, 400))

    all_sprites.draw(screen)
    pygame.display.update()
    clock.tick(60)  # Cap at 60 FPS for consistent movement

# Quit Pygame
pygame.quit()
sys.exit()
