import pygame
import sys
import json
import random
from mylib import reset, visitedall, prov
from character import Character
from fireball import Fireball
from my_challenges import fireball_challenge_logic



# -------------------
# Load Room Data
# -------------------
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
clock = pygame.time.Clock()  # Add a clock for consistent frame rate

# -------------------
# Game Setup
# -------------------

# Start in the first room (top left of the map)
where = list(north.keys())[0]
prov(where, visited, image_and_caption)

# Create player character
player = Character(role="PC", color=(255, 0, 0))
player.move_to_center()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# set up fireballs for the Fireball Challenge room
fireballs = pygame.sprite.Group()
fireball_timer = 0
dodged_fireballs = 0
dodge_target = 30
dodge_goal_achieved = False  # permanent flag for duration of this game

running = True
game_over = False

# -------------------
# Main Game Loop
# -------------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Global reset (r) and quit (q) keys
            if event.key == pygame.K_r:
                where = reset(where, visited, image_and_caption)
                player.move_to_center()
                player.health = 10
                game_over = False
                fireballs.empty()

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
        # Room Boundary Check
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
            fireballs.empty()
            
            if where in game_end_locations:
                game_over = True
                player.move_to_center()
            else:
                player.move_to_edge("right")


        elif player.rect.right > right_bound:
            next_room = east[where]
            where = next_room
            prov(where, visited, image_and_caption)
            fireballs.empty()
            
            if where in game_end_locations:
                game_over = True
                player.move_to_center()
            else:
                player.move_to_edge("left")

        elif player.rect.top < top_bound:
            next_room = north[where]
            where = next_room
            prov(where, visited, image_and_caption)
            fireballs.empty()
            
            if where in game_end_locations:
                game_over = True
                player.move_to_center()
            else:
                player.move_to_edge("down")

        elif player.rect.bottom > bottom_bound:
            next_room = south[where]
            where = next_room
            prov(where, visited, image_and_caption)
            fireballs.empty()
            
            if where in game_end_locations:
                game_over = True
                player.move_to_center()
            else:
                player.move_to_edge("up")

        # -------------------
        # Fireball Challenge (Tomb of the Forgotten)
        # -------------------
        if where == "Tomb of the Forgotten":
            fireball_challenge_things = fireball_challenge_logic(
                where, player, fireballs, fireball_timer, dodged_fireballs,
                dodge_target, dodge_goal_achieved, prov, visited, image_and_caption
            )
            fireball_timer = fireball_challenge_things["fireball_timer"]
            dodged_fireballs = fireball_challenge_things["dodged_fireballs"]
            dodge_goal_achieved = fireball_challenge_things["dodge_goal_achieved"]
            game_over_flag = fireball_challenge_things["game_over_flag"]

    # -------------------
    # Drawing
    # -------------------
    screen.fill(white)
    screen.blit(image_and_caption["current_image"], (200, 100))
    caption_text = font.render(image_and_caption["current_caption"], True, black)
    screen.blit(caption_text, (300, 400))

    all_sprites.draw(screen)
    fireballs.draw(screen)
    health_text = font.render("Health: " + str(player.health), True, (200, 0, 0))
    screen.blit(health_text, (10, 10))
    if where == "Tomb of the Forgotten":
        target_text = font.render("Target: Dodge 30 fireballs", True, (0, 0, 0))
        dodged_text = font.render("Dodged: " + str(min(dodged_fireballs, dodge_target)), True, (0, 128, 0))
        screen.blit(target_text, (10, 40))
        screen.blit(dodged_text, (10, 70))

    pygame.display.update()
    clock.tick(60)  # Cap at 60 FPS for consistent movement

# Quit Pygame
pygame.quit()
sys.exit()
