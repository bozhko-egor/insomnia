import pygame
from pygame.locals import *
from src.menus import TempScreen, MenuGameState, MenuItem
from src.gamestates import GameState
from src.platforms import *
from src.editor.text_input import TextInput
from .errors import NoSuchLevel


class MainEditorMenu(MenuGameState):

    def __init__(self, engine):
        GameState.__init__(self, engine)
        self.engine = engine
        self.menu_items = ('Create New Level', 'Load Level', "Quit")
        self.menu_func = {'Create New Level': self.engine.to_new_level,
                          'Load Level': self.engine.to_level_input,
                          'Quit': self.exit}
        self.font = pygame.font.SysFont("monospace", 50)
        self.bg_color = (88, 88, 88)
        self.font_color = (0, 0, 0)
        self.items = []
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.cur_item = 0
        if type(self) == MainEditorMenu:
            self.setup_menu()


class MenuItemWithPic(MenuItem):

    def __init__(self, *args):
        super().__init__(*args)
        self.image = None


class PauseScreen(MainEditorMenu):

    def __init__(self, *args):
        super().__init__(*args)
        self.menu_items = ('Platform', 'AlarmClock', 'PowerUp', 'ExitBlock', 'SlowDown', 'WindArea', 'Teleport', 'SpawnPoint')
        self.blocks = {x: globals()[x] for x in self.menu_items}
        self.menu_func = {x: self.engine.to_editor_with_block(self.blocks[x]) for x in self.menu_items}
        self.menu_func.update({'Save Level': self.engine.to_save_level,
                               'To menu': self.engine.to_menu,
                               'Quit': self.exit})
        self.menu_items += ('Save Level', 'To menu', 'Quit')

        self.setup_menu()

    def draw(self):
        self.timer.tick(60)
        self.screen.fill(self.bg_color)
        for item in self.items:
            x, y = item.position
            self.screen.blit(item.label, (x, y))
            if item.image:
                self.screen.blit(item.image, (500, y))

    def setup_menu(self):
        for index, item in enumerate(self.menu_items):
            menu_item = MenuItemWithPic(item)
            platform = self.blocks.get(item, None)
            if platform:
                if platform == Teleport:
                    menu_item.image = platform(self, 0, 0, 0).image
                else:
                    menu_item.image = platform(self, 0, 0).image
            t_h = len(self.menu_items) * menu_item.height
            pos_x = (self.width / 2) - (menu_item.width / 2)
            pos_y = (self.height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
            if menu_item.text == 'Back':  # display *back* 100 units options below others
                pos_y += 100
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
        self.set_item_colors()  # set initial colors
        self.items[self.cur_item].set_font_color((255, 0, 0))


class EnterLevel(MainEditorMenu):

    def __init__(self, *args):
        super().__init__(*args)
        self.text_input = TextInput(self, 225, 200)
        self.menu_items = ('Load', 'Back')
        self.menu_func = {'Load': self.get_level_name,
                          'Back': self.engine.to_menu}
        self.setup_menu()
        self.err_msg = []
        self.time = 0
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)

    def draw(self):
        super().draw()
        for error in self.err_msg[:]:
            msg, t = error
            if self.time < t:
                label = self.font.render(msg, 1, (0, 0, 0))
                self.screen.blit(label, (25, 0))
            else:
                self.err_msg.remove(error)
        label = self.font.render('Enter level name:', 1, (0, 0, 0))
        self.screen.blit(label, (75, 150))
        if self.cur_item == 0:
            self.text_input.draw()

    def input(self, event):
        super().input(event)
        if event.type == pygame.USEREVENT + 1:
            self.time += 0.5
        if self.cur_item == 0:
            self.text_input.input(event)

    def get_level_name(self):
        name = ''.join(self.text_input.stack)
        try:
            self.engine.load_level(name)
        except NoSuchLevel:
            self.err_msg.append(('Error: No such level', self.time + 2))


class SaveLevel(MainEditorMenu):

    def __init__(self, *args):
        super().__init__(*args)
        self.text_input = TextInput(self, 225, 200)
        self.menu_items = ('Save', 'Back',)
        self.menu_func = {'Save': self.get_level_name,
                          'Back': self.engine.to_pause}

        self.setup_menu()
        self.err_msg = []
        self.time = 0
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)

    def draw(self):
        super().draw()
        for error in self.err_msg[:]:
            msg, t = error
            if self.time < t:
                label = self.font.render(msg, 1, (0, 0, 0))
                self.screen.blit(label, (25, 0))
            else:
                self.err_msg.remove(error)
        label = self.font.render('Enter name:', 1, (0, 0, 0))
        self.screen.blit(label, (75, 150))
        if self.cur_item == 0:
            self.text_input.draw()

    def input(self, event):
        super().input(event)
        if event.type == pygame.USEREVENT + 1:
            self.time += 0.5
        if self.cur_item == 0:
            self.text_input.input(event)

    def get_level_name(self):
        name = ''.join(self.text_input.stack)
        self.engine.save_level(name)
        with open('src/levels/level_list.txt', 'a') as file:
            file.writelines(name + '\n')
        self.err_msg.append(('Done!', self.time + 1))
