import pygame
from pygame import *
from src.editor.menu import MainEditorMenu, PauseScreen
from src.editor.editor_gamestate import EditorState

class LevelEditor:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Level editor")
        self.current_state = 0
        self.state_list = [MainEditorMenu,
                           EditorState,
                           PauseScreen]
        self.states = [x(self) for x in self.state_list]

    def main_loop(self):
        while True:
            self.states[self.current_state].draw()
            self.states[self.current_state].update()
            for event in pygame.event.get():
                self.states[self.current_state].input(event)

    def to_editor(self):
        self.current_state = 1

    def to_pause(self):
        self.current_state = 2

    def to_editor_with_block(self, block):
        def block_func():
            self.states[1].player.current_block = block(self.states[1], 0, 0)
            self.current_state = 1
        return block_func

if __name__ == '__main__':
    LevelEditor().main_loop()
