import pygame
from pygame import *
from src.gamestates import PlayGameState, InfiniteGameState
from src.menus import PauseGameState, MenuGameState, \
    TempScreen, DeathScreenState, RoundWinScreen, ModeScreen, LevelList, \
    OptionsScreen, DifficultyInfiniteMenu, PlayerSelectScreen
from src.level_config import levels
from src.player import PlayerAnimated
import pickle
import os


class GameEngine:
    """
    Main сlass with game loop.

    Handles gamestate switching.
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("v.0.03a")
        try:
            with open("src/saves/playerdata", "rb") as f:
                self.game_data = pickle.load(f)
        except FileNotFoundError:
            if not os.path.exists('src/saves/'):
                os.makedirs('src/saves/')
            self.reset_highscores()
        self.current_state = 0
        self.state_list = [MenuGameState,
                           PlayGameState,
                           PauseGameState,
                           TempScreen,
                           DeathScreenState,
                           RoundWinScreen,
                           ModeScreen,
                           LevelList,
                           OptionsScreen,
                           DifficultyInfiniteMenu,
                           PlayerSelectScreen]
        self.states = [x(self) for x in self.state_list]
        

    def main_loop(self):
        while True:
            self.states[self.current_state].draw()
            self.states[self.current_state].update()
            for event in pygame.event.get():
                self.states[self.current_state].input(event)

    def redraw_state(self, number, *args):
        self.states[number] = self.state_list[number](self, *args)
        self.current_state = number

    def previous_menu(self, menu):
        switch = {TempScreen: self.to_menu,
                  OptionsScreen: self.to_menu,
                  DifficultyInfiniteMenu: self.to_mode_screen,
                  LevelList: self.to_mode_screen,
                  ModeScreen: self.to_menu}
        back_func = switch.get(type(menu), None)
        if back_func is None:
            return None
        back_func()

    def to_game(self):
        self.current_state = 1

    def to_menu(self):
        self.redraw_state(0)

    def to_pause(self):
        self.redraw_state(2)

    def to_temp(self):
        self.redraw_state(3)

    def new_game(self):
        self.redraw_state(1)

    def to_animated(self):
        level = self.states[1].level
        self.states[1] = PlayGameState(self, player=PlayerAnimated, level=level)
        self.current_state = 1

    def to_death_screen(self, player):
        if type(player.gamestate) == InfiniteGameState:
            lvl = player.gamestate.level_number
            if player.score > self.game_data['infinite'][lvl]['highscore']:
                self.game_data['infinite'][lvl]['highscore'] = player.score
                if self.game_data['infinite'][lvl]['highscore'] > 100:
                    if lvl + 1 in self.game_data['infinite']:
                        self.game_data['infinite'][lvl + 1]['open'] = True

            self.save_player_data()
        self.redraw_state(4)

    def to_win_menu(self):
        game = self.states[1]
        lvl = game.level_number
        if game.player.score > self.game_data['storymode'][lvl]['highscore']:
            self.game_data['storymode'][lvl]['highscore'] = game.player.score
        if lvl + 1 in self.game_data['storymode']:
            self.game_data['storymode'][lvl + 1]['open'] = True

        self.save_player_data()
        self.redraw_state(5)

    def to_next_lvl(self):
        lvl = self.states[1].level_number
        lvl += 1
        if lvl > len(levels) - 1:
            lvl = 0
        self.redraw_state(1, type(self.states[1].player), levels[lvl])

    def replay_lvl(self):
        if type(self.states[1]) == PlayGameState:
            lvl = self.states[1].level

            self.states[1] = PlayGameState(self, type(self.states[1].player), level=lvl)
        elif type(self.states[1]) == InfiniteGameState:
            self.states[1] = InfiniteGameState(self)
        self.current_state = 1

    def to_mode_screen(self):
        self.redraw_state(6)

    def to_specific_lvl(self, level):
        def level_func():
            self.states[1] = self.state_list[1](self, level=level)
            self.current_state = 10
        return level_func

    def to_level_list(self):
        self.redraw_state(7)

    def to_options_screen(self):
        self.current_state = 8

    def to_diff_infinite_menu(self):
        self.redraw_state(9)

    def to_infinite_game(self):
        self.states[1] = InfiniteGameState(self)
        self.current_state = 1

    def to_player_select(self):
        self.redraw_state(10)

    def save_player_data(self):
        with open("src/saves/playerdata", "wb") as f:
            pickle.dump(self.game_data, f)

    def last_completed_lvl(self, menu):
        last_lvl = 0
        if type(menu) == LevelList:
            data = self.game_data['storymode']
            for i, _ in enumerate(levels):
                if data[i]['open']:
                    last_lvl = i
        elif type(menu) == DifficultyInfiniteMenu:
            data = self.game_data['infinite']
            for i in range(5):
                if data[i]['open']:
                    last_lvl = i
        return last_lvl

    def reset_highscores(self):
        self.game_data = {'storymode': {},
                          'infinite': {}}
        for i, _ in enumerate(levels):
            self.game_data['storymode'].update({i: {'highscore': 0,
                                                    'open': False}})
        for j in range(5):
            self.game_data['infinite'].update({j: {'highscore': 0,
                                                   'open': False}})
        self.game_data['storymode'][0]['open'] = True
        self.game_data['infinite'][0]['open'] = True
        self.save_player_data()


if __name__ == "__main__":
    GameEngine().main_loop()
