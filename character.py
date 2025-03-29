import pygame

# how to use for more player types
# npc = Character(role="NPC", color=(0, 0, 255))
# clone = Character(role="CloneBoost", color=(0, 255, 0))

class Character(pygame.sprite.Sprite):
    def __init__(self, role="PC", color=(255, 0, 0), position=(400, 220)):
        super().__init__()
        self.role = role  # "PC", "NPC", "CloneBoost", etc.
        self.color = color
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (10, 10), 10)
        self.rect = self.image.get_rect(center=position)
        self.speed = 8  # pixels per frame
        self.direction = pygame.Vector2(0, 0)

    def move_to_center(self):
        self.rect.center = (400, 220)

    # def set_direction(self, keys):
    #     self.direction = pygame.Vector2(0, 0)
    #     if keys[pygame.K_RIGHT]:
    #         self.direction.x = 1
    #     elif keys[pygame.K_LEFT]:
    #         self.direction.x = -1
    #     if keys[pygame.K_UP]:
    #         self.direction.y = -1
    #     elif keys[pygame.K_DOWN]:
    #         self.direction.y = 1

    """Place player at near edge of new room based on movement direction."""
    def move_to_edge(self, from_direction):
        if from_direction == "left":
            self.rect.left = 200  # enter from left → appear at left edge
        elif from_direction == "right":
            self.rect.right = 600  # enter from right → appear at right edge
        elif from_direction == "up":
            self.rect.top = 100  # enter from top → appear at top edge
        elif from_direction == "down":
            self.rect.bottom = 340  # enter from bottom → appear at bottom edge

    def update(self):
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y
        self.direction = pygame.Vector2(0, 0)  # reset after each move


