import pygame
from pygame.locals import *
from src.gamestates import GameState


class TextInput:

    def __init__(self, state, x, y, w=200, h=50):
        self.state = state
        self.image = pygame.Surface((w, h))
        self.image.fill((255, 255, 255))
        self.rect = Rect(x, y, w, h)
        self.font = pygame.font.SysFont('monospace', 45)
        self.stack = []

    def draw(self):
        label = self.font.render(''.join(self.stack), 1, (0, 0, 0))
        self.state.screen.blit(self.image, (self.rect.left, self.rect.top))
        self.state.screen.blit(label, (self.rect.left, self.rect.top))

    def update(self):
        self.timer.tick(60)
        pygame.display.update()

    def input(self, event):
        if event.type == QUIT:
            self.exit()
        if event.type == KEYDOWN:
            if chr(event.key) in 'abcdefghijklmnopqrstuvwxyz0123456789':
                if len(self.stack) > 6:
                    return
                self.stack.append(chr(event.key))

            if event.key == K_BACKSPACE:
                if len(self.stack) == 0:
                    return
                self.stack.pop()
