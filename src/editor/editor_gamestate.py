import pygame
from pygame.locals import *
from src.gamestates import GameState, OffsetCamera
from .dummy_player import DummyPlayer
from src.platforms import Platform


class EditorState(GameState):

    def __init__(self, engine, player=DummyPlayer):
        super().__init__(engine)
        self.bg = pygame.Surface((32, 32))
        self.grid_bg = pygame.Surface((32, 32))
        for i in [self.bg, self.grid_bg]:
            i.convert()
            i.fill(Color("#666666"))
        pygame.draw.line(self.grid_bg, (0, 0, 0), (0, 0), (0, 31), 1)
        self.entities = pygame.sprite.Group()
        self.player = player(32, 32, self)
        self.platforms = []
        self.camera = OffsetCamera(self.complex_camera, 640, 10**6)
        self.entities.add(self.player)
        self.up = self.down = self.left = self.right = False
        self.time = 0
        self.message_screen = []
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)

    def build_level(self, layout):
        for platform in layout:
            p_type, rect = platform
            x, y, w, h = rect.left, rect.top, rect.width, rect.height
            block = p_type(self, x, y, w=w, h=h)
            self.entities.add(block)
            self.platforms.append(block)

    def draw(self):
        for y in range(32):
            for x in range(21):
                self.screen.blit(self.bg, (x * 32, y * 32))
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))
        for i, message in enumerate(self.message_screen[:]):
            msg, time = message
            if self.time < time:
                label = self.player.font.render(msg, 1, (0, 0, 0))
                self.screen.blit(label, (175, 30 + i * 15))
            else:
                self.message_screen.remove(message)

    def update(self):
        self.timer.tick(60)
        self.camera.update(self.player)
        self.player.update(self.up, self.down, self.left, self.right, self.platforms)
        pygame.display.flip()

    def input(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.time += 0.5
        if event.type == QUIT:
            self.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.up = True
            elif event.key == K_DOWN:
                self.down = True
            elif event.key == K_LEFT:
                self.left = True
            elif event.key == K_RIGHT:
                self.right = True
            elif event.key == K_ESCAPE:
                self.engine.to_pause()
            elif event.key == K_SPACE:
                self.add_block()
            elif event.key == K_c:
                self.player.collision = not(self.player.collision)  # collision toggler
            elif event.key == K_i:
                self.player.in_increments = not(self.player.in_increments)
            elif event.key == K_g:
                self.draw_grid()
            elif event.key == K_w:
                self.make_wall_on_this_screen()
            elif event.key == K_z:
                self.undo_last_action()
            elif event.key == K_t:
                self.player.t_move = not(self.player.t_move)
        if event.type == KEYUP:
            if event.key == K_UP:
                self.up = False
            elif event.key == K_DOWN:
                self.down = False
            elif event.key == K_RIGHT:
                self.right = False
            elif event.key == K_LEFT:
                self.left = False

    def add_block(self):
        if not self.player.current_block:
            self.message_screen.append(('Select block by pressing Esc', self.time + 2))
            return
        block = type(self.player.current_block)(self,
                                                self.player.rect.left,
                                                self.player.rect.top)
        self.entities.add(block)  # probably need to add collision
        self.platforms.append(block)

    def draw_grid(self):
        self.bg, self.grid_bg = self.grid_bg, self.bg

    def make_wall_on_this_screen(self):
        def cycle(_x, _y):
            if (_x, _y) not in [(x.rect.left, x.rect.top) for x in self.platforms if type(x) == Platform]:
                block = Platform(self, _x, _y)
                self.entities.add(block)
                self.platforms.append(block)

        rect = self.camera.state
        y = - (rect.top - rect.top % 32)

        for y_new in range(25):
            cycle(0, y_new * 32 + y)
            cycle(608, y_new * 32 + y)

        if not y:
            for i in range(18):
                cycle((i + 1) * 32, 0)

    def undo_last_action(self):
        if self.platforms:
            self.entities.remove(self.platforms.pop())

    def complex_camera(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + self.width // 2, -t + self.height // 2

        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width - self.width), l)   # stop scrolling at the right edge
        t = max(-(camera.height - self.height), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        return Rect(l, t, w, h)
