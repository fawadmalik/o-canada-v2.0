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

image_and_caption = {"current_image": "","current_caption": ""}


# Define keypress flags
ise = False
isw = False
isn = False
iss = False

# Define colours
black = (0, 0, 0)
white = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("O Canada!")

#bc()
where = "bc"
prov(where,visited,image_and_caption)

# Set up font for captions
font = pygame.font.SysFont(None, 36)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Check for keypress events
    if where=="water" or where == "usa":
         keys = pygame.key.get_pressed()
         #press R to reset
         if keys[pygame.K_r]:
              reset(where, visited, image_and_caption)
    else:
         keys = pygame.key.get_pressed()
         if keys[pygame.K_e] and not ise:
              where = east[where]
              prov(where,visited,image_and_caption)
              ise = True
              
         if not keys[pygame.K_e]:
              ise = False

         if keys[pygame.K_w] and not isw:
              where = west[where]
              prov(where,visited,image_and_caption)
              isw = True
              
         if not keys[pygame.K_w]:
              isw = False

         if keys[pygame.K_n] and not isn:
              where = north[where]
              prov(where,visited,image_and_caption)
              isn = True

         if not keys[pygame.K_n]:
              isn = False


         if keys[pygame.K_s] and not iss:
              where = south[where]
              prov(where,visited,image_and_caption)
              iss = True

         if not keys[pygame.K_s]:
              iss = False


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
