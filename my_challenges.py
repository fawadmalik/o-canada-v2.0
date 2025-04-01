import random
import pygame
from fireball import Fireball

# -------------------
# Fireball Challenge
# -------------------
def fireball_challenge_logic(where, player, fireballs, fireball_timer, dodged_fireballs,
                              dodge_target, dodge_goal_achieved, prov, visited, image_and_caption):
    if where != "Tomb of the Forgotten":
        return fireball_timer, dodged_fireballs, dodge_goal_achieved, False

    if not dodge_goal_achieved:
        fireball_timer += 1
        if fireball_timer > 15:
            x = random.randint(210, 590)
            speed = random.choice([2, 4, 6, 10])
            fireball = Fireball(x, speed)
            fireballs.add(fireball)
            fireball_timer = 0

    # Update fireballs and track dodges
    for fireball in fireballs.sprites():
        if not dodge_goal_achieved:
            fireball.update()
        if fireball.rect.top > 340:
            fireball.kill()
            if not dodge_goal_achieved:
                dodged_fireballs += 1
                if dodged_fireballs >= dodge_target:
                    dodge_goal_achieved = True
                    fireballs.empty()

    # Detect collision only before goal is achieved
    if not dodge_goal_achieved:
        hits = pygame.sprite.spritecollide(player, fireballs, True)
        if hits:
            player.health -= 1
            if player.health <= 0:
                where = "hell"
                prov(where, visited, image_and_caption)
                player.move_to_center()
                fireballs.empty()
                return fireball_timer, dodged_fireballs, dodge_goal_achieved, True

    fireball_challenge_things = {"fireball_timer": fireball_timer, "dodged_fireballs": dodged_fireballs,
                                 "dodge_goal_achieved": dodge_goal_achieved, "game_over_flag": False}

    return fireball_challenge_things
