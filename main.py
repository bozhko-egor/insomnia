import pygame
from pygame import *
from src.gamestates import PlayGameState


class GameEngine:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("v.0.01a")
        self.states = [PlayGameState()]
        self.current_state = 0

    def main_loop(self):
        while True:
            self.states[self.current_state].draw()
            self.states[self.current_state].update()
            for event in pygame.event.get():
                self.states[self.current_state].input(event)


if __name__ == "__main__":
    GameEngine().main_loop()
