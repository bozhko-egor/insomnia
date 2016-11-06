import pygame
import sys
from pygame.locals import *
from src.player import Player
from src.levels import level1
from src.platforms import Platform, AlarmClock
from src.gametext import PlayerInfoText


class OffsetCamera:

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class PlayGameState:

    def __init__(self):
        self.screen_res = (640, 800)
        self.depth = 32
        self.flags = 0
        self.screen = pygame.display.set_mode(self.screen_res, self.flags, self.depth)
        self.timer = pygame.time.Clock()
        self.bg = pygame.Surface((32, 32))
        self.bg.convert()
        self.bg.fill(Color("#000000"))
        self.entities = pygame.sprite.Group()
        self.player = Player(32, 32)
        self.platforms = []
        self.level = level1
        self.build_level(self.level)
        total_level_width = len(self.level[0])*32
        total_level_height = len(self.level)*32
        self.camera = OffsetCamera(self.complex_camera, total_level_width, total_level_height)
        self.entities.add(self.player)
        self.text = PlayerInfoText(self.player, 500, 50, "monospace", 17)
        self.up = self.down = self.left = self.right = False

    def build_level(self, level):
        x = y = 0
        for row in level:
            for col in row:
                if col == "P":
                    p = Platform(x, y)
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "A":
                    clock = AlarmClock(x, y)
                    self.platforms.append(clock)
                    self.entities.add(clock)
                x += 32
            y += 32
            x = 0

    def draw(self):
        self.timer.tick(60)
        for y in range(32):
            for x in range(32):
                self.screen.blit(self.bg, (x * 32, y * 32))
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))

    def update(self):
        self.camera.update(self.player)
        self.text.update(self.screen)
        self.player.update(self.up, self.down, self.left, self.right, self.platforms)
        pygame.display.update()

    def input(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.up = True
            elif event.key == K_DOWN:
                self.down = True
            elif event.key == K_LEFT:
                self.left = True
            elif event.key == K_RIGHT:
                self.right = True

        if event.type == KEYUP:
            if event.key == K_UP:
                self.up = False
            elif event.key == K_DOWN:
                self.down = False
            elif event.key == K_RIGHT:
                self.right = False
            elif event.key == K_LEFT:
                self.left = False

    def complex_camera(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l + self.screen_res[0] // 2, -t + self.screen_res[1] // 2, w, h

        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width - self.screen_res[0]), l)   # stop scrolling at the right edge
        t = max(-(camera.height - self.screen_res[1]), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        return Rect(l, t, w, h)
