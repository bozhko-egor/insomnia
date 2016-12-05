import pygame
from pygame.locals import *
from src.menus import MenuGameState, MenuItem
import json

class TextQuest(MenuGameState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("src/scenes/replies.json") as f:
            self.choice_dict = json.load(f)
        self.current_reply = self.choice_dict
        self.font = pygame.font.SysFont("monospace", 25)
        self.replies = []
        self.time = 0
        self.replies_time_stack = []
        self.redraw()
        pygame.time.set_timer(pygame.USEREVENT + 2, 500)

    def draw(self):
        super().draw()
        count = -1
        for i, msg in enumerate(self.replies[:]):
            label = self.font.render(msg, 1, (255, 255, 255))
            self.screen.blit(label, (75, 30 + i * 25))
            count = i
        if self.time % 1000:
            msg2 = '>'
        else:
            msg2 = '>_'
        label2 = self.font.render(msg2, 1, (255, 255, 255))
        self.screen.blit(label2, (75, 30 + (count + 1) * 25))

    def input(self, event):
        super().input(event)
        if event.type == pygame.USEREVENT + 2:
            self.time += 500

    def update(self):
        pygame.display.update()
        for msg, time in self.replies_time_stack[:]:
            if time < self.time:
                self.replies.append(msg)
                self.replies_time_stack.remove((msg, time))

    def redraw(self):
        q, a = self.get_values()
        self.replies_time_stack.append(('> ' + q, self.time + 2000))
        self.menu_items = a
        self.menu_func = {x: self.add_reply(x) for x in self.menu_items}
        self.setup_menu()

    def add_reply(self, answer):
        def set_answer(*args, **kwargs):
            q, _ = self.get_values()
            self.current_reply = self.current_reply[q][answer]
            self.replies.append('> ' + answer)
            self.items = []
            self.redraw()
        return set_answer

    def get_values(self):
        question = list(self.current_reply.keys())[0]
        answers = list(self.current_reply[question].keys())
        return question, answers

    def setup_menu(self):
        for index, item in enumerate(self.menu_items):
            menu_item = MenuItem(item)
            t_h = len(self.menu_items) * menu_item.height
            pos_x = (self.width / 2) - (menu_item.width / 2)
            pos_y = (self.height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height) + 200
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
        self.set_item_colors()  # set initial colors
        self.items[self.cur_item].set_font_color((255, 0, 0))
