import pygame
import sys
from pygame.locals import *
from src.player import Player
from src.level_config import levels
from src.platforms import Platform, AlarmClock, PowerUp, SlowDown, ExitBlock
from src.gametext import PlayerInfoText


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

    def __init__(self, engine, level_number=0):
        super().__init__(engine)
        self.bg = pygame.Surface((32, 32))
        self.bg.convert()
        self.bg.fill(Color("#000000"))
        self.entities = pygame.sprite.Group()
        self.player = Player(32, 32, self)
        self.platforms = []
        self.level_effects = levels[level_number][1]
        self.level_number = level_number
        self.level = levels[level_number][0]
        self.build_level(self.level)
        total_level_width = len(self.level[0]) * 32
        total_level_height = len(self.level) * 32
        self.camera = OffsetCamera(self.complex_camera, total_level_width, total_level_height)
        self.entities.add(self.player)
        self.text = PlayerInfoText(self.player, 500, 50, "monospace", 17)
        self.up = self.down = self.left = self.right = False
        pygame.time.set_timer(pygame.USEREVENT + 1, 250)

    def build_level(self, level):
        x = y = 0
        for row in level:
            for col in row:
                platform_switch = {"P": Platform,
                                   "A": AlarmClock,
                                   "U": PowerUp,
                                   "S": SlowDown,
                                   "E": ExitBlock}
                plat_class = platform_switch.get(col, None)
                if plat_class:
                    p = plat_class(x, y)
                    self.platforms.append(p)
                    self.entities.add(p)
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
        if event.type == pygame.USEREVENT + 1:
            self.player.timer += 0.25
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
        self.menu_items = ('New game', 'Highscores', 'Options', "About", 'Quit')
        self.menu_func = {'New game': self.engine.new_game,
                          'Highscores': self.engine.to_temp,
                          'Options': self.engine.to_temp,
                          'About': self.engine.to_temp,
                          'Quit': self.exit}
        self.font_color = (255, 255, 255)
        self.items = []
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.cur_item = None
        if type(self) == MenuGameState:
            self.setup_menu()

    def draw(self):
        self.timer.tick(60)
        self.screen.fill(self.bg_color)
        for item in self.items:
            self.screen.blit(item.label, item.position)

    def update(self):
        pygame.display.update()

    def input(self, event):
        if event.type == QUIT:
            self.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.cur_item is None:
                    return
                chosen_func = self.menu_func.get(self.menu_items[self.cur_item])
                chosen_func()
            else:
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

    def setup_menu(self):
        for index, item in enumerate(self.menu_items):
            menu_item = MenuItem(item)
            t_h = len(self.menu_items) * menu_item.height
            pos_x = (self.width / 2) - (menu_item.width / 2)
            pos_y = (self.height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

    def display_temporary_screen(self):
        pass


class TempScreen(MenuGameState):

    def __init__(self, *args):
        super().__init__(*args)
        self.menu_items = ('Back',)
        self.menu_func = {'Back': self.engine.to_menu}
        self.font = pygame.font.SysFont("monospace", 45)
        self.setup_menu()

    def draw(self):
        super().draw()
        label = self.font.render('Nothing here yet!', 1, (0, 255, 0))
        self.screen.blit(label, (100, 150))


class DeathScreenState(MenuGameState):

    def __init__(self, *args):
        super().__init__(*args)
        self.menu_items = ('Retry?', 'No, thanks')
        self.menu_func = {'Retry?': self.engine.new_game,
                          'No, thanks': self.engine.to_menu}
        self.font = pygame.font.SysFont("monospace", 50)
        self.setup_menu()

    def draw(self):
        super().draw()
        label = self.font.render('YOU DIED', 1, (255, 0, 0))
        self.screen.blit(label, (200, 150))


class PauseGameState(MenuGameState):

    def __init__(self, *args):
        super().__init__(*args)
        self.menu_items = ('Continue', 'Restart level', 'To menu', 'Exit')
        self.menu_func = {'Continue': self.engine.to_game,
                          'Restart level': self.engine.replay_lvl,
                          'To menu': self.engine.to_menu,
                          'Exit': self.exit}
        self.font = pygame.font.SysFont("monospace", 50)
        self.setup_menu()

    def input(self, event):
        super().input(event)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.engine.to_game()

    def draw(self):
        super().draw()
        label = self.font.render('Paused', 1, (255, 0, 0))
        self.screen.blit(label, (235, 150))


class RoundWinScreen(MenuGameState):

    def __init__(self, *args):
        super().__init__(*args)
        self.menu_items = ('Next level', 'Replay level', 'Menu')
        self.menu_func = {'Next level': self.engine.to_next_lvl,
                          'Replay level': self.engine.replay_lvl,
                          'Menu': self.engine.to_menu}
        self.font = pygame.font.SysFont("monospace", 50)
        self.setup_menu()
