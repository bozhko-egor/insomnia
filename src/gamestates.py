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
        if event.type == QUIT:
            self.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.engine.current_state = 0


class MenuItem(pygame.font.Font):

    def __init__(self, text, font=None, font_size=55,
                 font_color=(255, 255, 255)):
        super().__init__(font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.pos_x = 0
        self.pos_y = 0
        self.position = self.pos_x, self.pos_y

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb):
        self.font_color = rgb
        self.label = self.render(self.text, 1, self.font_color)


class MenuGameState(GameState):

    def __init__(self, *args):
        super().__init__(*args)
        self.bg_color = (0, 0, 0)
        self.menu_items = ('New game', 'Highscores', 'Options', "Credits", 'Quit')
        self.font_color = (255, 255, 255)
        self.items = []
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.cur_item = None
        for index, item in enumerate(self.menu_items):
            menu_item = MenuItem(item)
            t_h = len(self.menu_items) * menu_item.height
            pos_x = (self.width / 2) - (menu_item.width / 2)
            pos_y = (self.height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

    def draw(self):
        self.timer.tick(60)
        self.screen.fill(self.bg_color)
        for item in self.items:
            self.screen.blit(item.label, item.position)
        pygame.display.update()

    def update(self):
        pass

    def input(self, event):
        if event.type == QUIT:
            self.exit()
        if event.type == pygame.KEYDOWN:
            self.set_keyboard_selection(event.key)

    def set_keyboard_selection(self, key):
        for item in self.items:
            item.set_font_color((255, 255, 255))

        if self.cur_item is None:
            self.cur_item = 0
        else:
            if key == pygame.K_UP and self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and self.cur_item == len(self.items) - 1:
                self.cur_item = 0

        self.items[self.cur_item].set_font_color((255, 0, 0))
