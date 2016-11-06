import pygame
import sys
from pygame.locals import *
from src.player import Player
from src.levels import level1
from src.platforms import Platform, AlarmClock, PowerUp
from src.gametext import PlayerInfoText, PauseText


class OffsetCamera:

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class GameState:

    def __init__(self, engine):
        self.engine = engine
        self.width = 640
        self.height = 800
        self.screen_res = (self.width, self.height)
        self.depth = 32
        self.flags = 0
        self.screen = pygame.display.set_mode(self.screen_res, self.flags, self.depth)
        self.timer = pygame.time.Clock()

    def exit(self):
        pygame.quit()
        sys.exit()


class PlayGameState(GameState):

    def __init__(self, *args):
        super().__init__(*args)
        self.bg = pygame.Surface((32, 32))
        self.bg.convert()
        self.bg.fill(Color("#000000"))
        self.entities = pygame.sprite.Group()
        self.player = Player(32, 32, self)
        self.platforms = []
        self.level = level1
        self.build_level(self.level)
        total_level_width = len(self.level[0]) * 32
        total_level_height = len(self.level) * 32
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
                if col == "U":
                    pu = PowerUp(x, y)
                    self.platforms.append(pu)
                    self.entities.add(pu)
                x += 32
            y += 32
            x = 0

    def draw(self):
        for y in range(32):
            for x in range(32):
                self.screen.blit(self.bg, (x * 32, y * 32))
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))

    def update(self):
        self.timer.tick(60)
        self.camera.update(self.player)
        self.text.update(self.screen)
        self.player.update(self.up, self.down, self.left, self.right, self.platforms)
        pygame.display.update()

    def input(self, event):
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
                self.engine.current_state = 1
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
        l, t = -l + self.width // 2, -t + self.height // 2

        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width - self.width), l)   # stop scrolling at the right edge
        t = max(-(camera.height - self.height), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        return Rect(l, t, w, h)


class DeathScreenState(GameState):

    def __init__(self, *args):
        super().__init__(*args)

    def draw(self):
        pass

    def update(self):
        pass

    def input(self):
        pass


class PauseGameState(GameState):

    def __init__(self, *args):
        super().__init__(*args)
        self.text = PauseText(250, 200, "monospace", 45)

    def draw(self):
        pass

    def update(self):
        self.text.update(self.screen)
        pygame.display.update()

    def input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.engine.current_state = 0


class MenuGameState(GameState):

    def __init__(self, *args):
        super().__init__(*args)

    def draw(self):
        pass

    def update(self):
        pass

    def input(self):
        pass
