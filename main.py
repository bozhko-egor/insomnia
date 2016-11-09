import pygame
from pygame import *
from src.gamestates import PlayGameState, InfiniteGameState
from src.menus import PauseGameState, MenuGameState, \
    TempScreen, DeathScreenState, RoundWinScreen, ModeScreen, LevelList, \
    OptionsScreen, DifficultyInfiniteMenu
from src.level_config import levels
import pickle


class GameEngine:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("v.0.03a")
        try:
            with open("src/saves/playerdata", "rb") as f:
                self.game_data = pickle.load(f)
        except FileNotFoundError:
            self.reset_highscores()
        self.state = MenuGameState(self)
        self.states = [MenuGameState(self),
                       PlayGameState(self),
                       PauseGameState(self),
                       TempScreen(self),
                       DeathScreenState(self),
                       RoundWinScreen(self),
                       ModeScreen(self),
                       LevelList(self),
                       OptionsScreen(self),
                       DifficultyInfiniteMenu(self)]
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
        game = self.states[1]
        lvl = game.level_number
        if game.player.score > self.game_data['storymode'][lvl]['highscore']:
            self.game_data['storymode'][lvl]['highscore'] = game.player.score
        if lvl + 1 in self.game_data['storymode']:
            self.game_data['storymode'][lvl + 1]['open'] = True

        self.save_player_data()
        self.states[5] = RoundWinScreen(self)
        self.current_state = 5

    def to_next_lvl(self):
        lvl = self.states[1].level_number
        lvl += 1
        if lvl > len(levels) - 1:
            lvl = 0
        self.states[1] = PlayGameState(self, lvl)
        self.current_state = 1

    def replay_lvl(self):
        if type(self.states[1]) == PlayGameState:
            lvl = self.states[1].level
            self.states[1] = PlayGameState(self, lvl)
        elif type(self.states[1]) == InfiniteGameState:
            self.states[1] = InfiniteGameState(self)
        self.current_state = 1

    def to_mode_screen(self):
        self.current_state = 6

    def to_specific_lvl(self, level):
        def level_func():
            self.states[1] = PlayGameState(self, level)
            self.current_state = 1
        return level_func

    def to_level_list(self):
        self.states[7] = LevelList(self)
        self.current_state = 7

    def to_options_screen(self):
        self.current_state = 8

    def to_diff_infinite_menu(self):
        self.current_state = 9

    def to_infinite_game(self):
        self.states[1] = InfiniteGameState(self)
        self.current_state = 1

    def save_player_data(self):
        with open("src/saves/playerdata", "wb") as f:
            pickle.dump(self.game_data, f)

    def last_completed_lvl(self):
        data = self.game_data['storymode']
        last_lvl = 0
        for i, _ in enumerate(levels):
            if data[i]['open']:
                last_lvl = i
        return last_lvl

    def reset_highscores(self):
        self.game_data = {'storymode': {}}
        for i, _ in enumerate(levels):
            self.game_data['storymode'].update({i: {'highscore': 0,
                                                    'open': False}
                                                })
        self.game_data['storymode'][0]['open'] = True
        self.save_player_data()


if __name__ == "__main__":
    GameEngine().main_loop()
