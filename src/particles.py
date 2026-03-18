import pygame

vec = pygame.math.Vector2


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, vel, size, color, gravity):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = vec(pos)
        self.vel = vec(vel)
        self.gravity = gravity
        self.opacity = 255

    def update(self):
        self.pos += self.vel
        self.vel.y += self.gravity
        self.rect.topleft = self.pos
        self.image.set_alpha(self.opacity)
        self.opacity -= 12
        if self.opacity <= 0:
            self.kill()
