import pygame
from pygame import *
from src.editor.menu import MainEditorMenu, PauseScreen, EnterLevel, SaveLevel
from src.editor.editor_gamestate import EditorState
import pickle
from src.editor.errors import NoSuchLevel
import os


class LevelEditor:

    def __init__(self):
        if not os.path.exists('src/levels'):
            os.makedirs('src/levels')
        pygame.init()
        pygame.display.set_caption("Level editor")
        self.current_state = 1
        self.state_list = [EditorState,
                           MainEditorMenu,
                           PauseScreen,
                           EnterLevel,
                           SaveLevel]
        self.states = [x(self) for x in self.state_list]

    def main_loop(self):
        while True:
            self.states[self.current_state].draw()
            self.states[self.current_state].update()
            for event in pygame.event.get():
                self.states[self.current_state].input(event)

    def save_level(self, name):
        level_data = [[type(x), x.rect] for x in self.states[0].platforms]
        with open("src/levels/{}".format(name), "wb") as f:
            pickle.dump(level_data, f)

    def load_level(self, name):
        try:
            with open("src/levels/{}".format(name), "rb") as f:
                level = pickle.load(f)
        except FileNotFoundError:
            raise NoSuchLevel
        self.states[0] = EditorState(self)
        self.states[0].build_level(level)
        self.current_state = 0

    def to_level_input(self):
        self.current_state = 3

    def to_menu(self):
        self.current_state = 1

    def to_editor(self):
        self.current_state = 0

    def to_pause(self):
        self.current_state = 2

    def to_save_level(self):
        self.current_state = 4

    def to_editor_with_block(self, block):
        def block_func():
            self.states[0].player.current_block = block(self.states[0], 0, 0)
            self.current_state = 0
        return block_func

if __name__ == '__main__':
    LevelEditor().main_loop()
