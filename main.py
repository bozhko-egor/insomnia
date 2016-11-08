import pygame
from pygame import *
from src.gamestates import PlayGameState, PauseGameState, MenuGameState, TempScreen, DeathScreenState, RoundWinScreen
from src.level_config import levels


class GameEngine:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("v.0.02a")
        self.state = MenuGameState(self)
        self.states = [MenuGameState(self),
                       PlayGameState(self),
                       PauseGameState(self),
                       TempScreen(self),
                       DeathScreenState(self),
                       RoundWinScreen(self)]
        self.current_state = 0

    def main_loop(self):
        while True:
            self.states[self.current_state].draw()
            self.states[self.current_state].update()
            for event in pygame.event.get():
                self.states[self.current_state].input(event)

    def to_game(self):
        self.current_state = 1

    def to_menu(self):
        self.states[0] = MenuGameState(self)
        self.current_state = 0

    def to_pause(self):
        self.current_state = 2

    def to_temp(self):
        self.current_state = 3

    def new_game(self):
        self.states[1] = PlayGameState(self)
        self.current_state = 1

    def to_death_screen(self):
        self.current_state = 4

    def to_win_menu(self):
        self.states[5] = RoundWinScreen(self)
        self.current_state = 5

    def to_next_lvl(self):
        lvl = self.states[1].level_number
        lvl += 1
        if lvl > len(levels[lvl][0]) - 1:
            lvl = 0
        self.states[1] = PlayGameState(self, lvl)
        self.current_state = 1

    def replay_lvl(self):
        lvl = self.states[1].level_number
        self.states[1] = PlayGameState(self, lvl)
        self.current_state = 1

if __name__ == "__main__":
    GameEngine().main_loop()
