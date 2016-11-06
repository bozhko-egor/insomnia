import pygame
from pygame import *


class Text:

    def __init__(self, x, y, font_name, font_size):
        self.x_coord = x
        self.y_coord = y
        self.font = pygame.font.SysFont(font_name, font_size)


class PlayerInfoText(Text):

    def __init__(self, player, *args):
        super().__init__(*args)
        self.player = player

    def update(self, screen):
        level_msg = "Level: {}".format(self.player.level)
        score_msg = "Score: {}".format(self.player.score)
        lives_msg = "Lives: {}".format(self.player.lives)
        for i, msg in enumerate([level_msg, score_msg, lives_msg]):
            label = self.font.render(msg, 1, (255, 255, 255))
            screen.blit(label, (self.x_coord, self.y_coord + i*15))
