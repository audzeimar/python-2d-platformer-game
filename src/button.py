import pygame


class Button:
    def __init__(self, x, y, width, height, text, image_path, sound_path=None):
        self.text = text
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(width), int(height)))
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        self.sound = pygame.mixer.Sound(sound_path) if sound_path else None

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.text:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'button': self}))
