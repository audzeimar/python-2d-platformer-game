import math
import random
import pygame

from assets import image_path, map_path, music_path
from camera import Camera
from death_animation import Death
from particles import Particle
from player import Player
from settings import WIDTH, HEIGHT, TILE_SIZE
from utils import Util

vec = pygame.math.Vector2
util = Util()


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, img_path):
        super().__init__()
        self.image = util.load_image(img_path, (width, height))
        self.rect = self.image.get_rect(topleft=pos)


class Step(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, img_path):
        super().__init__()
        self.image = util.load_image(img_path, (width, height // 2))
        self.rect = self.image.get_rect(topleft=pos)


class Spike(Block):
    def __init__(self, pos, width, height, img_path, rotate=False):
        super().__init__(pos, width, height, img_path)
        if rotate:
            self.image = pygame.transform.rotate(self.image, 180)


class Game:
    def __init__(self, map_file="map.txt"):
        self.blocks = pygame.sprite.Group()
        self.steps = pygame.sprite.Group()
        self.death_ani = pygame.sprite.GroupSingle()
        self.particles = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.map = self.read_file(map_path(map_file))
        self.map_width = len(self.map[0]) * TILE_SIZE
        self.map_height = len(self.map) * TILE_SIZE
        self.camera = Camera(self.map_width, self.map_height)
        self.game_over = False
        self.status = ""
        self.level_end = 0

        self.bg = pygame.image.load(image_path("bg.png")).convert()
        self.bg_width = self.bg.get_width()
        self.tiles = math.ceil(WIDTH / self.bg_width) + 1
        self.scroll_position = 0

        self.death_sound = pygame.mixer.Sound(music_path("Death Sound2.mp3"))
        self.level_music = music_path("Forever_Bound-Stereo_Madness_(Geometry_Dash)-world75.spcs.bio.mp3")

        self.load_map()
        self.start_music()

    def start_music(self):
        pygame.mixer.music.load(self.level_music)
        pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    @staticmethod
    def read_file(path):
        with open(path, "r", encoding="utf-8") as file:
            return file.read().splitlines()

    def load_map(self):
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                pos = (x * TILE_SIZE, y * TILE_SIZE)
                if char == "B":
                    self.blocks.add(Block(pos, TILE_SIZE, TILE_SIZE, image_path("block.png")))
                elif char == "P":
                    self.player.add(Player(pos, TILE_SIZE, TILE_SIZE, image_path("player.png")))
                elif char == "S":
                    self.spikes.add(Spike((x * TILE_SIZE + 2, y * TILE_SIZE + 4), TILE_SIZE - 4, TILE_SIZE - 4, image_path("spike.png")))
                elif char == "R":
                    self.spikes.add(Spike(pos, TILE_SIZE, TILE_SIZE - 4, image_path("spike.png"), True))
                elif char == "T":
                    self.steps.add(Step(pos, TILE_SIZE, TILE_SIZE, image_path("STEP1.PNG")))
                elif char == "W":
                    self.level_end = x * TILE_SIZE

    def update_status(self):
        if self.player.sprite and self.player.sprite.pos.x >= self.level_end:
            self.status = "Level completed"

    def horizontal_movement(self):
        player = self.player.sprite
        player.pos.x += player.direction.x
        player.hit_rect.x = player.pos.x
        for obstacle in [*self.blocks, *self.steps]:
            if obstacle.rect.colliderect(player.hit_rect):
                self.game_over = True
                player.hit_rect.right = obstacle.rect.left
                player.pos.x = player.hit_rect.x

        if pygame.sprite.spritecollide(player, self.spikes, False, pygame.sprite.collide_mask):
            self.game_over = True

    def vertical_movement(self):
        player = self.player.sprite
        player.apply_gravity()
        for obstacle in [*self.blocks, *self.steps]:
            if obstacle.rect.colliderect(player.hit_rect):
                if player.direction.y < 0:
                    self.game_over = True
                    player.hit_rect.top = obstacle.rect.bottom
                    player.pos.y = player.hit_rect.y
                    player.direction.y = 0
                elif player.direction.y > 0:
                    player.on_ground = True
                    player.hit_rect.bottom = obstacle.rect.top
                    player.pos.y = player.hit_rect.y
                    player.direction.y = 0

        if (player.on_ground and player.direction.y < 0) or player.direction.y > 0:
            player.on_ground = False

    def check_game_over(self):
        if self.game_over and self.player.sprite:
            self.stop_music()
            self.death_sound.play()
            self.death_ani.add(Death(self.camera.apply(self.player.sprite.rect).center))
            self.player.sprite.kill()

    def update(self):
        player = self.player.sprite
        if player:
            if player.on_ground:
                particle_pos = self.camera.apply(player.rect).bottomleft + vec(3, -6)
                particle_vel = (random.uniform(-4.5, -0.5), random.uniform(-0.8, -0.5))
                self.particles.add(Particle(particle_pos, particle_vel, 7, "white", 0.1))
            self.horizontal_movement()
            self.vertical_movement()
            self.camera.update(player.rect)
            self.update_status()
            self.check_game_over()
            if not self.game_over:
                self.scroll_position -= 5
                if abs(self.scroll_position) > self.bg_width:
                    self.scroll_position = 0

        self.player.update()
        self.death_ani.update()
        self.particles.update()

    def draw(self, surface):
        for i in range(self.tiles):
            surface.blit(self.bg, (i * self.bg_width + self.scroll_position, 0))

        self.particles.draw(surface)
        for block in self.blocks:
            surface.blit(block.image, self.camera.apply(block.rect))
        for spike in self.spikes:
            surface.blit(spike.image, self.camera.apply(spike.rect))
        for step in self.steps:
            surface.blit(step.image, self.camera.apply(step.rect))
        if self.player.sprite:
            surface.blit(self.player.sprite.image, self.camera.apply(self.player.sprite.rect))
        self.death_ani.draw(surface)


def run_game(screen, clock):
    game = Game("map.txt")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if game.game_over and game.death_ani.sprite is None:
            return True

        screen.fill("white")
        game.update()
        game.draw(screen)
        pygame.display.update()
        clock.tick(60)
