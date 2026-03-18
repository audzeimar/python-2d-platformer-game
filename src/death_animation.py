import pygame


class Death(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((300, 300), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.opacity = 255
        self.radius = 0

    def update(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(
            self.image,
            (142, 142, 142, self.opacity),
            (self.image.get_width() // 2, self.image.get_height() // 2),
            self.radius,
        )
        self.radius += 3
        self.opacity -= 6
        if self.opacity <= 0 or self.radius >= self.image.get_width() // 2:
            self.kill()
