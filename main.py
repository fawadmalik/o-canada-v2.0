import pygame
import sys
import json
from mylib import reset, visitedall, prov

# Load data from JSON file
with open("rooms.json", "r") as file:
    data = json.load(file)

# Accessing the dictionaries
east = data["east"]
west = data["west"]
north = data["north"]
south = data["south"]
visited = data["visited"]

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

# bc()
where = "bc"
prov(where, visited, image_and_caption)

# Set up font for captions
font = pygame.font.SysFont(None, 36)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if where == "water" or where == "usa":
        keys = pygame.key.get_pressed()
        # press R to reset
        if keys[pygame.K_r]:
            where = reset(where, visited, image_and_caption)
            print(where + "::" + str(image_and_caption))

        if keys[pygame.K_q]:
            running = False
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not is_right:
            where = east[where]
            prov(where, visited, image_and_caption)
            is_right = True

        if not keys[pygame.K_RIGHT]:
            is_right = False

        if keys[pygame.K_LEFT] and not is_left:
            where = west[where]
            prov(where, visited, image_and_caption)
            is_left = True

        if not keys[pygame.K_LEFT]:
            is_left = False

        if keys[pygame.K_UP] and not is_up:
            where = north[where]
            prov(where, visited, image_and_caption)
            is_up = True

        if not keys[pygame.K_UP]:
            is_up = False

        if keys[pygame.K_DOWN] and not is_down:
            where = south[where]
            prov(where, visited, image_and_caption)
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

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
