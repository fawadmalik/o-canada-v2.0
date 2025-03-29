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
game_end_location = ["hell"]

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
    if where in game_end_location:
        keys = pygame.key.get_pressed()
        # press R to reset
        if keys[pygame.K_r]:
            where = reset(where, visited, image_and_caption)
            player.move_to_center()
            # print(where + "::" + str(image_and_caption))

        if keys[pygame.K_q]:
            running = False
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not is_right:
            where = east[where]
            prov(where, visited, image_and_caption)
            player.move_to_center()
            is_right = True

        if not keys[pygame.K_RIGHT]:
            is_right = False

        if keys[pygame.K_LEFT] and not is_left:
            where = west[where]
            prov(where, visited, image_and_caption)
            player.move_to_center()
            is_left = True

        if not keys[pygame.K_LEFT]:
            is_left = False

        if keys[pygame.K_UP] and not is_up:
            where = north[where]
            prov(where, visited, image_and_caption)
            player.move_to_center()
            is_up = True

        if not keys[pygame.K_UP]:
            is_up = False

        if keys[pygame.K_DOWN] and not is_down:
            where = south[where]
            prov(where, visited, image_and_caption)
            player.move_to_center()
            is_down = True

        if not keys[pygame.K_DOWN]:
            is_down = False

        if keys[pygame.K_r]:
            where = reset(where, visited, image_and_caption)

        if keys[pygame.K_q]:
            running = False

    # Display the current image

    screen.fill(white)  # Fill the screen with white
    screen.blit(image_and_caption["current_image"], (200, 100))

    # Render the caption text
    caption_text = font.render(image_and_caption["current_caption"], True, black)
    screen.blit(caption_text, (300, 400))

    all_sprites.update()
    all_sprites.draw(screen)
    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
