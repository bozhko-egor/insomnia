import pygame
import sys
from pygame.locals import *
from .player import Player, PlayerAnimated, OfficePlayer
from .level_config import levels
from .platforms import Platform, AlarmClock, PowerUp, SlowDown, ExitBlock, MovingPlatform, WindArea, Teleport
from .gametext import PlayerInfoText


class OffsetCamera:

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class GameState:
    """Basic Gamestate class that every state inherits from."""

    def __init__(self, engine):
        self.engine = engine
        self.width = 640
        self.height = 800
        self.screen_res = (self.width, self.height)
        self.depth = 32
        self.flags = 0
        self.screen = pygame.display.set_mode(self.screen_res, self.flags, self.depth)
        self.timer = pygame.time.Clock()

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()


class PlayGameState(GameState):
    """Represents storymode gamestate."""

    def __init__(self, engine, player=Player, level=levels[0]):
        super().__init__(engine)
        self.bg = pygame.image.load('src/sprites/backgrounds/background.png')
        self.entities = pygame.sprite.Group()
        self.platforms = []
        self.platforms_collider = []
        self.level = level
        self.build_level(level.level)
        # self.background_audio = pygame.mixer.Sound(file='src/audio/1.wav')
        # self.background_audio.play(loops=-1)
        self.player = player(64, 64, self)
        self.level_effects = [x(self.player) for x in level.effects]
        self.level_number = level.number
        self.camera = OffsetCamera(self.complex_camera, self.level_width, self.level_height)
        self.entities.add(self.player)
        self.text = PlayerInfoText(self.player, 500, 50, "monospace", 17)
        self.up = self.down = self.left = self.right = False

        pygame.time.set_timer(pygame.USEREVENT + 1, 100)

    def build_level(self, layout):
        max_w = 0
        max_h = 0
        for platform in layout:
            p_type, rect, args = platform
            x, y, w, h = rect.left, rect.top, rect.width, rect.height
            if y > max_h:
                max_h = y
            if x > max_w:
                max_w = x
            block = p_type(self, x, y, *args, w=w, h=h)
            self.platforms.append(block)
            self.entities.add(block)
        self.level_width = max_w + 32
        self.level_height = max_h + 32

    def draw(self):
        img_height = self.bg.get_height()
        diff = img_height - self.height
        diff2 = self.level_height - self.height  # background parallax
        dy = diff2 // diff
        y = self.camera.state.top // dy
        self.screen.blit(self.bg, (0, y))
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))

    def update(self):
        for p in self.entities:
            if type(p) in [Player, PlayerAnimated, OfficePlayer]:
                continue
            p.update()
        self.timer.tick(60)
        self.camera.update(self.player)
        self.text.update(self.screen)
        self.player.update(self.up, self.down, self.left, self.right, self.platforms)
        pygame.display.flip()

    def input(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.player.timer += 0.1  # used in counting seconds
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
            elif event.key in [K_ESCAPE, K_p]:
                self.engine.to_pause()
            elif event.key == K_SPACE:
                if not self.player.item.cd_left:
                    self.player.item.turn_on()
            elif event.key == K_q:
                self.engine.to_win_menu()  # for testing purposes
            elif event.key == K_d:
                self.engine.to_death_screen(self.player)
            elif event.key == K_r:
                self.engine.replay_lvl()
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
