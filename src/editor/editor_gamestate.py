import pygame
from pygame.locals import *
from src.gamestates import GameState, OffsetCamera
from .dummy_player import DummyPlayer
from src.platforms import Platform, WindArea
from src.editor.menu import PauseScreen
from .arrows import Arrow
import time
import copy

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
            p_type, rect, args = platform
            x, y, w, h = rect.left, rect.top, rect.width, rect.height
            block = p_type(self, x, y, *args, w=w, h=h)
            self.entities.add(block)
            self.platforms.append(block)

    def draw(self):
        for y in range(32):
            for x in range(21):
                self.screen.blit(self.bg, (x * 32, y * 32))
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))
            if hasattr(e, 'arrow'):
                self.screen.blit(e.arrow.image, self.camera.apply(e.arrow))
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
                self.add_block(self.player.rect.left, self.player.rect.top)
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
            elif event.key == K_r:
                self.redo_last_action()
            elif event.key == K_q:
                self.setup_wind_block()
            elif chr(event.key) in ''.join([str(x) for x in range(1, 10)]):
                block_switch = {str(i + 1): name for i, name in enumerate(PauseScreen(self.engine).blocks.values())}
                print(block_switch)
                block = block_switch.get(chr(event.key), None)
                self.player.current_block = block(self, self.player.rect.left, self.player.rect.top)
            elif event.key == K_F5:
                self.quick_save()

        if event.type == KEYUP:
            if event.key == K_UP:
                self.up = False
            elif event.key == K_DOWN:
                self.down = False
            elif event.key == K_RIGHT:
                self.right = False
            elif event.key == K_LEFT:
                self.left = False

    def add_block(self, x, y):
        if not self.player.current_block:
            self.message_screen.append(('Select block by pressing Esc', self.time + 2))
            return
        block = type(self.player.current_block)(self,
                                                x,
                                                y,
                                                *self.player.current_block.args)
        block_current = self.player.current_block
        if hasattr(block_current, 'arrow'):
            dx = block_current.arrow.x - block_current.arrow.x1
            dy = block_current.arrow.y - block_current.arrow.y1
            arrow = Arrow(x, y, x - dx, y - dy)
            arrow.redraw()
            block.arrow = arrow

        self.entities.add(block)  # probably need to add collision
        self.platforms.append(block)

        return block

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

    def quick_save(self):
        name = time.strftime('%X')
        name = ''.join(name.split(':'))
        self.engine.save_level(name)

    def setup_wind_block(self):
        if len(self.platforms) >= 2:
            block1, block2 = self.platforms[-2:]
            if type(block1) == WindArea and type(block2) == WindArea:
                for i in range(2):
                    self.entities.remove(self.platforms.pop())
                self.player.current_block.args = [block2.rect.left, block2.rect.top]
                x = block1.rect.left
                y = block1.rect.top
                x1 = block2.rect.left
                y1 = block2.rect.top
                block = self.add_block(x, y)
                block.arrow = Arrow(x, y, x1, y1)
                block.arrow.redraw()

    def undo_last_action(self):
        if self.platforms:
            self.entities.remove(self.platforms.pop())

    def redo_last_action(self):
        if self.platforms:
            self.player.current_block = self.platforms[-1]

    def complex_camera(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + self.width // 2, -t + self.height // 2

        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width - self.width), l)   # stop scrolling at the right edge
        t = max(-(camera.height - self.height), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        return Rect(l, t, w, h)
