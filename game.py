import pygame
import sys
from pygame.locals import *


class Game:

    pygame.display.set_caption('testing stuff')

    def __init__(self):
        self.screen_res = [800, 600]
        self.screen = pygame.display.set_mode(self.screen_res)
        self.player = PlayerSprite(50, 50)
        self.player.game = self
        self.all_sprites_list = pygame.sprite.Group()
        self.all_sprites_list.add(self.player)
        self.clock = pygame.time.Clock()
        wall_list = pygame.sprite.Group()
        wall = Platform(0, 100, 400, 10)
        wall_list.add(wall)
        self.all_sprites_list.add(wall)
        self.player.walls = wall_list
        self.clock.tick(45)
        while True:
            self.main_loop()
            self.all_sprites_list.update()
            self.screen.fill((255, 255, 255))
            self.all_sprites_list.draw(self.screen)
            pygame.display.update()

    def main_loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.exit()
            if not hasattr(event, 'key'):
                continue
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.player.set_moving_speed(self.player.speed, 0)
                elif event.key == K_LEFT:
                    self.player.set_moving_speed(-self.player.speed, 0)
                elif event.key == K_UP:
                    self.player.set_moving_speed(0, -self.player.speed)
                elif event.key == K_DOWN:
                    self.player.set_moving_speed(0, self.player.speed)

            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.player.set_moving_speed(-self.player.speed, 0)
                elif event.key == K_LEFT:
                    self.player.set_moving_speed(self.player.speed, 0)
                elif event.key == K_UP:
                    self.player.set_moving_speed(0, self.player.speed)
                elif event.key == K_DOWN:
                    self.player.set_moving_speed(0, -self.player.speed)

    def exit(self):
        pygame.quit()
        sys.exit()


class PlayerSprite(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sample_image.png')
        self.speed = 2
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 1  # falling speed
        self.game = None
        self.walls = None

    def set_moving_speed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):
        scr_x, scr_y = self.game.screen_res
        self.rect.x += self.change_x
        if self.rect.x > scr_x + self.rect.width:
            self.rect.x = 0
        elif self.rect.x + self.rect.width < 0:
            self.rect.x = scr_x

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y
        if self.rect.y > scr_y + self.rect.height:
            self.rect.y = 0
        elif self.rect.y + self.rect.height < 0:
            self.rect.y = scr_y

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Platform(pygame.sprite.Sprite):

        def __init__(self, x, y, width, height):
            super().__init__()
            self.image = pygame.Surface([width, height])
            self.image.fill((0, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x


if __name__ == '__main__':
    pygame.init()
    Game()
