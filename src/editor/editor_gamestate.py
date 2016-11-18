import pygame
import sys
from pygame.locals import *
from src.gamestates import GameState, OffsetCamera
from .dummy_player import DummyPlayer
import pickle


class EditorState(GameState):
    """Represents storymode gamestate."""

    def __init__(self, engine, player=DummyPlayer):
        super().__init__(engine)
        self.bg = pygame.Surface((32, 32))
        self.bg.convert()
        self.entities = pygame.sprite.Group()
        self.player = player(32, 32, self)
        self.bg.fill(Color("#666666"))
        self.platforms = []
        self.camera = OffsetCamera(self.complex_camera, 640, 10**6)
        self.entities.add(self.player)
        self.up = self.down = self.left = self.right = False
        self.time = 0
        self.message_screen = []
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)

    def draw(self):
        for y in range(32):
            for x in range(32):
                self.screen.blit(self.bg, (x * 32, y * 32))
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))
        for i, message in enumerate(self.message_screen[:]):
            msg, time = message
            if self.time < time:
                label = self.player.font.render(msg, 1, (0, 0, 0))
                self.screen.blit(label, (175, 30 + i * 15))
            else:
                self.message_screen.remove(message)

    def update(self):
        self.timer.tick(60)
        self.camera.update(self.player)
        self.player.update(self.up, self.down, self.left, self.right, self.platforms)
        pygame.display.flip()

    def input(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.time += 0.5
        if event.type == QUIT:
            self.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.up = True
            elif event.key == K_DOWN:
                self.down = True
            elif event.key == K_LEFT:
                self.left = True
            elif event.key == K_RIGHT:
                self.right = True
            elif event.key == K_ESCAPE:
                self.engine.to_pause()
            elif event.key == K_SPACE:
                self.add_block()
        if event.type == KEYUP:
            if event.key == K_UP:
                self.up = False
            elif event.key == K_DOWN:
                self.down = False
            elif event.key == K_RIGHT:
                self.right = False
            elif event.key == K_LEFT:
                self.left = False

    def add_block(self):
        if not self.player.current_block:
            self.message_screen.append(('Select block by pressing Esc', self.time + 2))
            return
        block = type(self.player.current_block)(self,
                                                self.player.rect.left,
                                                self.player.rect.top)
        self.entities.add(block)  # probably need to add collision

    def save_level(self, name):
        level = (self.platforms, self.entities[:].remove(self.player))
        with open("src/editor/levels/{}".format(name), "wb") as f:
            pickle.dump(level, f)

    def load_level(self, name):
        with open("src/editor/levels/{}".format(name), "rb") as f:
            level = pickle.load(f)
        return level

    def complex_camera(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + self.width // 2, -t + self.height // 2

        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width - self.width), l)   # stop scrolling at the right edge
        t = max(-(camera.height - self.height), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        return Rect(l, t, w, h)
