import pygame
from pygame.locals import *
from src.platforms import AlarmClock, PowerUp


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, gamestate):
        super().__init__()
        self.gamestate = gamestate
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = pygame.Surface((32, 32))
        self.image.fill(Color("#00FF00"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
        self.score = 0
        self.pwup_score = 0
        self.lives = 3
        self.level = 1

    def update(self, up, down, left, right, platforms):
        if up:
            if self.onGround:
                self.yvel -= 10
        if down:
            pass
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            self.yvel += 0.3
            if self.yvel > 100:
                self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)
        self.score = self.pwup_score + self.rect.bottom // 100

    def collide(self, xvel, yvel, platforms):
        for p in platforms[:]:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, AlarmClock):
                    self.gamestate.engine.to_death_screen()
                    return
                if isinstance(p, PowerUp):
                    self.gamestate.platforms.remove(p)
                    self.gamestate.entities.remove(p)
                    self.pwup_score += 50
                    return
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.yvel = 0  # lose speed on *head* contact with platform
                    self.rect.top = p.rect.bottom
