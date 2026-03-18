import pygame
from settings import WIDTH, HEIGHT


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)

    def apply(self, target_rect):
        return target_rect.move(self.rect.topleft)

    def update(self, target_rect):
        x = -target_rect.centerx + WIDTH // 2
        y = -target_rect.centery + HEIGHT // 2
        x = min(x, 0)
        x = max(x, WIDTH - self.width)
        y = min(y, 0)
        y = max(y, HEIGHT - self.height)
        self.rect = pygame.Rect(x, y, self.width, self.height)
