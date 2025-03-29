import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, role="PC", color=(255, 0, 0), position=(400, 220)):
        super().__init__()
        self.role = role  # "PC", "NPC", "CloneBoost", etc.
        self.color = color
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (10, 10), 10)
        self.rect = self.image.get_rect(center=position)

    def move_to_center(self):
        self.rect.center = (400, 220)

    def move_to_edge(self, from_direction):
        """Place player at opposite edge of new room based on movement direction."""
        if from_direction == "left":
            self.rect.right = 600  # right edge of image
        elif from_direction == "right":
            self.rect.left = 200  # left edge
        elif from_direction == "up":
            self.rect.bottom = 340  # bottom edge
        elif from_direction == "down":
            self.rect.top = 100  # top edge

    def update(self):
        # Placeholder for movement, animation, AI, etc.
        pass

