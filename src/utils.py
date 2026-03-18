import pygame
from assets import font_path


class Util:
    @staticmethod
    def load_image(path, size=None, convert_alpha=True):
        image = pygame.image.load(path)
        image = image.convert_alpha() if convert_alpha else image.convert()
        if size:
            image = pygame.transform.scale(image, size)
        return image

    @staticmethod
    def draw_center_text(surface, text, pos, font_size, color):
        font = pygame.font.Font(font_path("Vera.ttf"), font_size)
        image = font.render(text, True, color)
        rect = image.get_rect(center=pos)
        surface.blit(image, rect)
