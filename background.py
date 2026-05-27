# background.py
import pygame
import math

SCROLL_SPEED = 5

# Colors
WALL_TOP     = (232, 192, 112)
WALL_MID     = (242, 212, 152)
WALL_BOT     = (242, 216, 152)
CEILING_COL  = (200, 144, 64)
CEILING_DARK = (176, 120, 40)
FLOOR_COL    = (139, 90,  43)
FLOOR_DARK   = (92,  58,  16)
FLOOR_MID    = (107, 68,  24)
BASE_COL     = (200, 160, 96)
BASE_DARK    = (160, 120, 64)
WIN_FRAME    = (200, 160, 96)
WIN_GLASS    = (154, 204, 224)
WIN_SHINE    = (200, 234, 248)
TREE_DARK    = (74,  154, 52)
TREE_LIGHT   = (90,  170, 68)
TRUNK        = (139, 90,  43)
CURTAIN      = (204, 68,  68)
CURTAIN_DARK = (170, 34,  34)
CURTAIN_LITE = (221, 85,  85)
ROD          = (139, 90,  43)
FRAME_GOLD   = (200, 160, 48)
FRAME_WOOD   = (122, 78,  24)
SHELF_COL    = (139, 90,  43)
SHELF_DARK   = (92,  58,  16)
RUG_BASE     = (153, 51,  34)
RUG_LIGHT    = (187, 68,  51)
RUG_STRIPE   = (204, 85,  68)
RUG_EDGE     = (119, 17,  34)
LAMP_POST    = (92,  58,  16)
LAMP_SHADE   = (255, 200, 80)


class Background:
    def __init__(self, width, height, ground_y):
        self.width        = width
        self.height       = height
        self.ground_y     = ground_y
        self.wall_offset  = 0
        self.floor_offset = 0

    def update(self):
        self.wall_offset  = (self.wall_offset  + SCROLL_SPEED // 2) % self.width
        self.floor_offset = (self.floor_offset + SCROLL_SPEED)      % 80

    def draw(self, surface):
        self._draw_wall(surface)
        self._draw_ceiling(surface)
        self._draw_windows(surface)
        self._draw_pictures(surface)
        self._draw_shelves(surface)
        self._draw_lamps(surface)
        self._draw_floor(surface)
        self._draw_baseboard(surface)
        self._draw_rugs(surface)

    def _draw_wall(self, surface):
        band = self.ground_y // 5
        colors = [WALL_TOP, (234, 200, 120), (238, 208, 128), (240, 212, 140), WALL_BOT]
        for i, col in enumerate(colors):
            pygame.draw.rect(surface, col, (0, i * band, self.width, band + 2))

    def _draw_ceiling(self, surface):
        pygame.draw.rect(surface, CEILING_COL,  (0, 0, self.width, 18))
        pygame.draw.rect(surface, CEILING_DARK, (0, 18, self.width, 5))

    def _draw_floor(self, surface):
        pygame.draw.rect(surface, FLOOR_COL,  (0, self.ground_y, self.width, self.height - self.ground_y))
        pygame.draw.rect(surface, (170, 112, 48), (0, self.ground_y, self.width, 4))
        plank = 100
        for x in range(-plank, self.width + plank, plank):
            px = (x - self.floor_offset) % (self.width + plank) - plank
            pygame.draw.line(surface, FLOOR_DARK, (px, self.ground_y), (px, self.height), 3)
        for yo in [22, 44, 66]:
            pygame.draw.line(surface, FLOOR_MID,
                             (0, self.ground_y + yo), (self.width, self.ground_y + yo), 1)

    def _draw_baseboard(self, surface):
        pygame.draw.rect(surface, BASE_COL,  (0, self.ground_y - 12, self.width, 12))
        pygame.draw.rect(surface, BASE_DARK, (0, self.ground_y - 4,  self.width, 4))

    def _draw_rugs(self, surface):
        for bx in [120, 580, 1040]:
            rx = (bx - self.wall_offset * 2) % (self.width + 500) - 250
            self._draw_rug(surface, rx)

    def _draw_rug(self, surface, x):
        ry = self.ground_y - 12
        rw, rh = 200, 10
        pygame.draw.rect(surface, RUG_BASE,   (x,      ry, rw, rh), 0, 2)
        pygame.draw.rect(surface, RUG_LIGHT,  (x + 4,  ry, rw - 8, rh // 2))
        for i in range(3):
            sx = x + 20 + i * 60
            pygame.draw.rect(surface, RUG_STRIPE, (sx, ry + 1, 40, rh - 2), 0, 2)
        pygame.draw.rect(surface, RUG_EDGE,   (x, ry, 8,  rh))
        pygame.draw.rect(surface, RUG_EDGE,   (x + rw - 8, ry, 8, rh))
        for fx in range(x, x + rw, 8):
            pygame.draw.line(surface, RUG_EDGE, (fx, ry + rh), (fx, ry + rh + 5), 1)

    def _draw_windows(self, surface):
        for bx in [200, 700]:
            wx = (bx - self.wall_offset) % (self.width + 400) - 200
            self._draw_window(surface, wx, 28)

    def _draw_window(self, surface, x, y):
        w, h = 130, 190
        # glass
        pygame.draw.rect(surface, WIN_GLASS, (x, y, w, h), 0, 2)
        # outside trees
        pygame.draw.rect(surface, TREE_DARK,  (x, y, w // 2, h // 2))
        pygame.draw.rect(surface, TREE_LIGHT, (x + w // 2, y, w // 2, h // 2))
        pygame.draw.rect(surface, TREE_LIGHT, (x, y + h // 2, w // 2, h // 2))
        pygame.draw.rect(surface, TREE_DARK,  (x + w // 2, y + h // 2, w // 2, h // 2))
        pygame.draw.rect(surface, TRUNK, (x + 22, y + h // 2 - 20, 8, 40))
        pygame.draw.rect(surface, TRUNK, (x + w - 30, y + h // 2 - 20, 8, 40))
        # shine
        pygame.draw.rect(surface, WIN_SHINE, (x + 4, y + 4, 6, 22))
        pygame.draw.rect(surface, WIN_SHINE, (x + 4, y + 4, 18, 5))
        # frame
        pygame.draw.rect(surface, WIN_FRAME, (x, y, w, h), 8, 2)
        pygame.draw.rect(surface, WIN_FRAME, (x + w // 2 - 4, y, 8, h))
        pygame.draw.rect(surface, WIN_FRAME, (x, y + h // 2 - 4, w, 8))
        # curtains
        pygame.draw.rect(surface, CURTAIN, (x - 18, y - 4, 24, h + 12), 0, 2)
        pygame.draw.rect(surface, CURTAIN_LITE, (x - 14, y, 10, h + 4))
        pygame.draw.rect(surface, CURTAIN, (x + w - 6, y - 4, 24, h + 12), 0, 2)
        pygame.draw.rect(surface, CURTAIN_LITE, (x + w - 2, y, 10, h + 4))
        for fy in range(y + 28, y + h, 44):
            pygame.draw.rect(surface, CURTAIN_DARK, (x - 18, fy, 24, 5))
            pygame.draw.rect(surface, CURTAIN_DARK, (x + w - 6, fy, 24, 5))
        pygame.draw.rect(surface, ROD, (x - 22, y - 6, w + 44, 7))
        pygame.draw.rect(surface, ROD, (x - 22, y - 6, 8, 12))
        pygame.draw.rect(surface, ROD, (x + w + 14, y - 6, 8, 12))

    def _draw_pictures(self, surface):
        for bx in [420, 980]:
            px = (bx - self.wall_offset) % (self.width + 500) - 250
            self._draw_picture(surface, px, 24)

    def _draw_picture(self, surface, x, y):
        fw, fh = 104, 80
        pygame.draw.rect(surface, FRAME_GOLD, (x, y, fw, fh), 0, 2)
        pygame.draw.rect(surface, FRAME_WOOD, (x + 4, y + 4, fw - 8, fh - 8), 0, 2)
        pygame.draw.rect(surface, (26, 42, 90), (x + 8, y + 8, fw - 16, fh - 16))
        pygame.draw.rect(surface, (26, 58, 122), (x + 8, y + 8, fw - 16, 24))
        pygame.draw.rect(surface, (45, 110, 45), (x + 8, y + 32, fw - 16, 16))
        pygame.draw.rect(surface, (170, 120, 48), (x + 8, y + 48, fw - 16, fh - 56))
        pygame.draw.rect(surface, (255, 238, 68), (x + 60, y + 12, 12, 12))
        pygame.draw.rect(surface, (255, 238, 68), (x + 56, y + 16, 20, 6))
        pygame.draw.rect(surface, (34, 85, 170),  (x + 10, y + 10, 4, 60))
        pygame.draw.rect(surface, (34, 85, 170),  (x + 10, y + 10, fw - 18, 4))

    def _draw_shelves(self, surface):
        for bx in [340, 880]:
            sx = (bx - self.wall_offset) % (self.width + 500) - 250
            self._draw_shelf(surface, sx, 148)

    def _draw_shelf(self, surface, x, y):
        w = 160
        pygame.draw.rect(surface, SHELF_COL,  (x, y, w, 12), 0, 2)
        pygame.draw.rect(surface, (170, 112, 48), (x, y, w, 5))
        pygame.draw.rect(surface, SHELF_DARK, (x, y + 8, w, 4))
        pygame.draw.rect(surface, SHELF_COL,  (x + 4,     y + 12, 10, 36))
        pygame.draw.rect(surface, SHELF_COL,  (x + w - 14, y + 12, 10, 36))
        book_colors = [(232, 68, 68), (68, 136, 238), (68, 187, 68),
                       (204, 136, 238), (238, 153, 34), (68, 136, 204)]
        bx = x + 10
        for i, bc in enumerate(book_colors):
            bw = 16
            bh = 28 + (i % 3) * 5
            pygame.draw.rect(surface, bc, (bx, y - bh, bw, bh), 0, 1)
            darker = tuple(max(0, c - 40) for c in bc)
            pygame.draw.line(surface, darker, (bx + 3, y - bh + 3), (bx + 3, y - 3), 1)
            bx += bw + 2
        # plant
        px = x + w - 28
        pygame.draw.polygon(surface, (170, 102, 34), [
            (px, y), (px + 20, y), (px + 16, y - 16), (px + 4, y - 16)])
        pygame.draw.rect(surface, (80, 50, 20), (px + 2, y - 18, 16, 5))
        for angle, length in [(-60, 20), (-90, 26), (-120, 20)]:
            rad = math.radians(angle)
            ex  = int(px + 10 + math.cos(rad) * length)
            ey  = int(y - 16 + math.sin(rad) * length)
            pygame.draw.line(surface, (34, 102, 34), (px + 10, y - 16), (ex, ey), 3)
            pygame.draw.circle(surface, (68, 170, 68), (ex, ey), 5)

    def _draw_lamps(self, surface):
        for bx in [820, 1380]:
            lx = (bx - self.wall_offset) % (self.width + 600) - 300
            self._draw_lamp(surface, lx)

    def _draw_lamp(self, surface, x):
        pygame.draw.rect(surface, LAMP_POST, (x, self.ground_y - 110, 6, 98))
        pygame.draw.rect(surface, LAMP_POST, (x - 10, self.ground_y - 14, 26, 8), 0, 3)
        pygame.draw.rect(surface, SHELF_DARK, (x - 12, self.ground_y - 12, 30, 4), 0, 2)
        pts = [(x - 18, self.ground_y - 110),
               (x + 24, self.ground_y - 110),
               (x + 14, self.ground_y - 138),
               (x - 8,  self.ground_y - 138)]
        pygame.draw.polygon(surface, LAMP_SHADE, pts)
        pygame.draw.polygon(surface, (255, 238, 102), [
            (pts[0][0] + 2, pts[0][1] + 2),
            (pts[1][0] - 2, pts[1][1] + 2),
            (pts[2][0], pts[2][1] + 2),
            (pts[3][0], pts[3][1] + 2)
        ])
        glow = pygame.Surface((70, 44), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (255, 240, 150, 50), (0, 0, 70, 44))
        surface.blit(glow, (x - 32, self.ground_y - 152))