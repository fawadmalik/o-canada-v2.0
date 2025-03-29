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

# game_end_location = ["water", "usa"]
game_end_locations = ["hell"]

image_and_caption = {"current_image": "", "current_caption": ""}

# Define keypress flags
is_right = False
is_left = False
is_up = False
is_down = False

# Define colours
black = (0, 0, 0)
white = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("O Canada!")

# Set up font for captions
font = pygame.font.SysFont(None, 36)

# -------------------
# Game Setup
# -------------------

# Start in the first room (top left of the map)
where = list(north.keys())[0]
prov(where, visited, image_and_caption)
print("Starting with image and caption of " + str(image_and_caption))

# Create player character
player = Character(role="PC", color=(255, 0, 0))
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if where in game_end_locations:
                if event.key == pygame.K_r:
                    where = reset(where, visited, image_and_caption)
                    player.move_to_center()
                elif event.key == pygame.K_q:
                    running = False

            else:
                if event.key == pygame.K_RIGHT:
                    player.direction.x = player.speed
                elif event.key == pygame.K_LEFT:
                    player.direction.x = -player.speed
                elif event.key == pygame.K_UP:
                    player.direction.y = -player.speed
                elif event.key == pygame.K_DOWN:
                    player.direction.y = player.speed
                elif event.key == pygame.K_r:
                    where = reset(where, visited, image_and_caption)
                    player.move_to_center()
                elif event.key == pygame.K_q:
                    running = False

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
        if next_room not in game_end_locations:
            where = next_room
            prov(where, visited, image_and_caption)
            player.move_to_edge("right")

        else:
            where = next_room
            prov(where, visited, image_and_caption)
            player.move_to_center()

    elif player.rect.right > right_bound:
        next_room = east[where]
        if next_room not in game_end_locations:
            where = next_room
            prov(where, visited, image_and_caption)
            player.move_to_edge("left")
        else:
            where = next_room
            prov(where, visited, image_and_caption)
            player.move_to_center()

    elif player.rect.top < top_bound:
        next_room = north[where]
        if next_room not in game_end_locations:
            where = next_room
            prov(where, visited, image_and_caption)
            player.move_to_edge("down")
        else:
            where = next_room
            prov(where, visited, image_and_caption)
            player.move_to_center()

    elif player.rect.bottom > bottom_bound:
        next_room = south[where]
        if next_room not in game_end_locations:
            where = next_room
            prov(where, visited, image_and_caption)
            player.move_to_edge("up")
        else:
            where = next_room
            prov(where, visited, image_and_caption)
            player.move_to_center()

    # -------------------
    # Drawing
    # -------------------
    screen.fill(white)
    screen.blit(image_and_caption["current_image"], (200, 100))
    caption_text = font.render(image_and_caption["current_caption"], True, black)
    screen.blit(caption_text, (300, 400))

    all_sprites.draw(screen)
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
