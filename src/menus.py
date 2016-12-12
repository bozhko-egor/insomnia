import pygame
from pygame.locals import *
from .level_config import levels
from .gamestates import GameState


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
        self.menu_func = {'New game': self.engine.to_mode_screen,
                          'Highscores': self.engine.to_temp,
                          'Options': self.engine.to_options_screen,
                          'About': self.engine.to_temp,
                          'Quit': self.exit}
        self.font_color = (255, 255, 255)
        self.items = []
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.cur_item = 0
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
        self.set_item_colors()
        if key == pygame.K_ESCAPE:
            self.engine.previous_menu(self)
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

    def set_item_colors(self):
        for i, item in enumerate(self.items):
                item.set_font_color(self.font_color)

    def setup_menu(self):
        for index, item in enumerate(self.menu_items):
            menu_item = MenuItem(item)
            t_h = len(self.menu_items) * menu_item.height
            pos_x = (self.width / 2) - (menu_item.width / 2)
            pos_y = (self.height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
            if menu_item.text == 'Back':  # display *back* 100 units options below others
                pos_y += 100
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
        self.set_item_colors()  # set initial colors
        self.items[self.cur_item].set_font_color((255, 0, 0))


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
        self.menu_func = {'Retry?': self.engine.replay_lvl,
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


class ModeScreen(MenuGameState):

    def __init__(self, *args):
        super().__init__(*args)
        self.menu_items = ('Levels', 'Infinite mode', "Back")
        self.menu_func = {'Levels': self.engine.to_level_list,
                          'Infinite mode': self.engine.to_diff_infinite_menu,
                          'Back': self.engine.to_menu}
        self.font = pygame.font.SysFont("monospace", 50)
        self.setup_menu()


class LevelList(MenuGameState):

    def __init__(self, *args):
        super().__init__(*args)
        self.menu_items = [str(x.number + 1) for x in levels]
        self.menu_items.append('Back')
        self.menu_func = {str(x.number + 1): self.engine.to_specific_lvl(x) for x in levels}
        self.menu_func.update({'Back': self.engine.to_mode_screen})
        self.font = pygame.font.SysFont("monospace", 50)
        self.last_lvl = self.engine.last_completed_lvl(self)
        self.hs_font = pygame.font.SysFont('monospace', 35)
        self.name = 'storymode'
        if type(self) == LevelList:
            self.setup_menu()

    def set_item_colors(self):
        for i, item in enumerate(self.items):
            if i <= self.last_lvl or i == len(self.items) - 1:
                item.set_font_color((255, 255, 255))
            elif len(self.items) - 1 > i > self.last_lvl:
                item.set_font_color((65, 65, 65))

    def input(self, event):
        if event.type == QUIT:
            self.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.cur_item is None:
                    return
                if len(self.items) - 1 > self.cur_item > self.last_lvl:
                    return  # do nothing on *enter* on uncompleted lvls
                chosen_func = self.menu_func.get(self.menu_items[self.cur_item])
                chosen_func()
            else:
                self.set_keyboard_selection(event.key)

    def draw(self):
        super().draw()
        self.show_highscores()

    def show_highscores(self):
        if self.cur_item is None:
            return
        if self.cur_item <= self.last_lvl:
            hs = self.engine.game_data[self.name][self.cur_item]['highscore']
            label = self.hs_font.render('Highscore: {}'.format(hs), 1, (255, 255, 255))
            self.screen.blit(label, (200, 100))


class OptionsScreen(MenuGameState):

    def __init__(self, *args):
        super().__init__(*args)
        self.menu_items = ('Reset data', 'Back')
        self.menu_func = {'Reset data': self.engine.reset_highscores,
                          'Back': self.engine.to_menu}
        self.font = pygame.font.SysFont("monospace", 50)
        self.setup_menu()


class DifficultyInfiniteMenu(LevelList):

    def __init__(self, *args):
        super().__init__(*args)
        self.menu_items = ('i can win', 'bring it on', 'hurt me plenty', 'hardcore', 'nightmare', 'Back')
        self.menu_func = {'i can win': self.engine.to_infinite_game,
                          'bring it on': self.engine.to_temp,
                          'hurt me plenty': self.engine.to_temp,
                          'hardcore': self.engine.to_temp,
                          'nightmare': self.engine.to_temp,
                          'Back': self.engine.to_mode_screen}
        self.setup_menu()
        self.name = 'infinite'


class PlayerSelectScreen(MenuGameState):

    def __init__(self, *args):
        super().__init__(*args)
        self.menu_items = ('Player', 'Animated Player', 'OfficePlayer', 'Back')
        self.menu_func = {'Player': self.engine.to_game,
                          'Animated Player': self.engine.to_animated,
                          'OfficePlayer': self.engine.to_office,
                          'Back': self.engine.to_menu}
        self.font = pygame.font.SysFont("monospace", 50)
        self.setup_menu()
