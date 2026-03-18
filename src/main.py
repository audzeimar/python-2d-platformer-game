import pygame
from menu import menu
from settings import WIDTH, HEIGHT, FPS, WINDOW_TITLE


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    running = menu(screen, clock)
    pygame.quit()
    return running


if __name__ == "__main__":
    main()
