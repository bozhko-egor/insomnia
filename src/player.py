import pygame
from pygame.locals import *
from src.platforms import AlarmClock, PowerUp, SlowDown, ExitBlock
from .effects import DefaultEffect


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
        self.timer = 0
        self.status_effects = []
        self.max_vel = 25
        self.max_depth = 0

    def update(self, up, down, left, right, platforms):
        self.check_status_effects()
        if not self.check_level_effects(up, down, left, right):  # using alternate mechanics
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
                if self.yvel > self.max_vel:
                    self.yvel = self.max_vel
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

        if self.max_depth < self.rect.bottom:
            self.max_depth = self.rect.bottom
        self.score = self.pwup_score + self.max_depth // 100

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
                if isinstance(p, SlowDown):
                    self.gamestate.platforms.remove(p)
                    self.gamestate.entities.remove(p)
                    effect = p.effect(self)
                    if not self.check_effect(effect):
                        effect.start_time = self.timer
                        self.status_effects.append(effect)
                    return
                if isinstance(p, ExitBlock):
                    self.gamestate.engine.to_win_menu()
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = 0  # remove xvel on contact
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = 0
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.yvel = 0  # lose speed on *head* contact with platform
                    self.rect.top = p.rect.bottom

    def check_effect(self, effect):
        for element in self.status_effects[:]:
            if type(effect) == type(element):
                element.duration += effect.duration
                return True
        return False

    def check_status_effects(self):
        for i, effect in enumerate(self.status_effects[:]):
            time_left = effect.duration - (self.timer - effect.start_time)
            effect.time_left = time_left
            if time_left > 0:
                effect.set_effect()
                effect.update(35, 35 + i * 15)
            else:
                self.status_effects.remove(effect)
                DefaultEffect(self).default_effects()

    def check_level_effects(self, *args):
        for i, effect in enumerate(self.gamestate.level_effects):
            effect.set_effect(*args)
            effect.update(35, 700 + i * 15)
        return bool(len(self.gamestate.level_effects))
