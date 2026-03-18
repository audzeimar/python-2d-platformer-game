import sys
import pygame

from assets import image_path, music_path
from button import Button
from game import run_game
from settings import WIDTH, HEIGHT, FPS


def menu(screen, clock):
    pygame.display.set_caption("Geometry Dash")
    menu_music = music_path("menu.mp3")
    click_sound = music_path("start.mp3")

    background = pygame.image.load(image_path("main_background.jpg")).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    logo_image = pygame.image.load(image_path("logo.png")).convert_alpha()
    logo_image = pygame.transform.scale(logo_image, (500, 370))
    logo_rect = logo_image.get_rect(topleft=(215, -100))

    start_button = Button(WIDTH / 2 - 85, HEIGHT / 2 - 85, 170, 170, "", image_path("play.png"), click_sound)
    exit_button = Button(WIDTH / 2 - 260, HEIGHT / 2 - 50, 100, 100, "", image_path("quit.png"), click_sound)
    settings_button = Button(WIDTH / 2 + 150, HEIGHT / 2 - 50, 100, 100, "", image_path("settings.png"), click_sound)

    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)

    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(logo_image, logo_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            start_button.handle_event(event)
            exit_button.handle_event(event)
            settings_button.handle_event(event)

            if event.type == pygame.USEREVENT and event.button == exit_button:
                return False
            if event.type == pygame.USEREVENT and event.button == start_button:
                pygame.mixer.music.stop()
                should_continue = run_game(screen, clock)
                if not should_continue:
                    return False
                pygame.mixer.music.load(menu_music)
                pygame.mixer.music.play(-1)
            if event.type == pygame.USEREVENT and event.button == settings_button:
                settings_menu(screen, clock, background, click_sound)

        settings_button.draw(screen)
        start_button.draw(screen)
        exit_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def settings_menu(screen, clock, background, click_sound):
    audio_button = Button(WIDTH / 2 - 130, 100, 270, 75, "audio", image_path("2.png"), click_sound)
    back_button = Button(WIDTH / 2 - 130, 200, 270, 75, "back", image_path("2.png"), click_sound)

    running = True
    while running:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            audio_button.handle_event(event)
            back_button.handle_event(event)
            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False

        audio_button.draw(screen)
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    return True
