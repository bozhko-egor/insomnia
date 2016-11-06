import pygame
from pygame import *
import sys
from levels import level1

WIDTH = 640
HEIGHT = 800
HALF_WIDTH = int(WIDTH / 2)
HALF_HEIGHT = int(HEIGHT / 2)

DISPLAY = (WIDTH, HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("testing")
    timer = pygame.time.Clock()

    up = down = left = right = False
    bg = Surface((32, 32))
    bg.convert()
    bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []

    x = y = 0
    level = level1

    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            x += 32
        y += 32
        x = 0

    total_level_width = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    while True:
        timer.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    up = True
                elif event.key == K_DOWN:
                    down = True
                elif event.key == K_LEFT:
                    left = True
                elif event.key == K_RIGHT:
                    right = True

            if event.type == KEYUP:
                if event.key == K_UP:
                    up = False
                elif event.key == K_DOWN:
                    down = False
                elif event.key == K_RIGHT:
                    right = False
                elif event.key == K_LEFT:
                    left = False

        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        player.update(up, down, left, right, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()


class Camera:

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32, 32))
        self.image.fill(Color("#00FF00"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

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

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
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


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)


if __name__ == "__main__":
    main()
