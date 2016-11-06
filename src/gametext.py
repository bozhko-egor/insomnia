import pygame
from pygame import *


class Text:

    def __init__(self, x, y, font_name, font_size):
        self.x_coord = x
        self.y_coord = y
        self.font = pygame.font.SysFont(font_name, font_size)

    def display_on_screen(self, screen, message, antialias, color, x, y):
        label = self.font.render(message, antialias, color)
        screen.blit(label, (x, y))


class PlayerInfoText(Text):

    def __init__(self, player, *args):
        super().__init__(*args)
        self.player = player

    def update(self, screen):
        level_msg = "Level: {}".format(self.player.level)
        score_msg = "Score: {}".format(self.player.score)
        lives_msg = "Lives: {}".format(self.player.lives)
        for i, msg in enumerate([level_msg, score_msg, lives_msg]):
            self.display_on_screen(screen, msg, 1, (255, 255, 255), self.x_coord, self.y_coord + i * 15)



class PauseText(Text):

    def update(self, screen):
        msg = "PAUSED"
        self.display_on_screen(screen, msg, 1, (255, 255, 255), self.x_coord, self.y_coord)
