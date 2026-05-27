# obstacles.py
import pygame
import random

# Colors
TRASH_BODY  = (85,  85,  85)
TRASH_LITE  = (119, 119, 119)
TRASH_DARK  = (51,  51,  51)
CHAIR_WOOD  = (139, 90,  43)
CHAIR_SEAT  = (170, 112, 48)
CHAIR_DARK  = (92,  58,  16)
TABLE_TOP   = (139, 90,  43)
TABLE_LITE  = (170, 112, 48)
TABLE_DARK  = (92,  58,  16)
CHEESE_YEL  = (245, 200, 0)
CHEESE_LITE = (255, 224, 51)
CHEESE_DARK = (196, 154, 0)
CHEESE_HOLE = (184, 136, 0)
SOFA_BODY   = (100, 60,  140)
SOFA_LITE   = (130, 85,  170)
SOFA_DARK   = (70,  35,  100)
SOFA_PILLOW = (220, 180, 255)
SHOE_BODY   = (60,  35,  15)
SHOE_SOLE   = (30,  20,  8)
SHOE_LITE   = (90,  55,  25)
VASE_BODY   = (200, 80,  40)
VASE_LITE   = (230, 110, 60)
VASE_DARK   = (150, 50,  20)
VASE_WATER  = (100, 180, 220)
FLOWER_STEM = (50,  130, 50)
FLOWER_PET  = (240, 80,  120)
FLOWER_CEN  = (255, 220, 50)
BROOM_STICK = (160, 100, 40)
BROOM_HEAD  = (200, 160, 80)
BROOM_DARK  = (140, 100, 40)
POT_BODY    = (180, 90,  50)
POT_DARK    = (130, 60,  30)
PLANT_GREEN = (50,  160, 50)
PLANT_DARK  = (30,  110, 30)


class Obstacle:
    KINDS = ["trashcan", "shoe", "vase", "broom", "flower_pot", "sofa"]

    def __init__(self, x, ground_y, kind=None):
        self.ground_y = ground_y
        self.kind     = kind or random.choice(self.KINDS)
        self._setup(x)

    def _setup(self, x):
        sizes = {
            "trashcan":   (46, 60),
            "shoe":       (80, 50),
            "vase":       (44, 72),
            "broom":      (28, 110),
            "flower_pot": (50, 80),
            "sofa":       (160, 90),
        }
        w, h = sizes[self.kind]
        self.rect = pygame.Rect(x, self.ground_y - h, w, h)

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        return self.rect.right > 0

    def draw(self, surface):
        getattr(self, f"_draw_{self.kind}")(surface)

    # ── TRASHCAN ──────────────────────────────────────────────────── #
    def _draw_trashcan(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        pygame.draw.rect(surface, TRASH_BODY,  (x+3, y+12, w-6, h-12), 0, 3)
        pygame.draw.rect(surface, TRASH_LITE,  (x+3, y+12, 5, h-12))
        pygame.draw.rect(surface, TRASH_LITE,  (x+3, y+12, w-6, 4))
        pygame.draw.rect(surface, TRASH_DARK,  (x+w-6, y+12, 5, h-12))
        for by in [y+26, y+42]:
            pygame.draw.rect(surface, TRASH_DARK, (x+3, by, w-6, 3))
        pygame.draw.line(surface, TRASH_LITE, (x+9, y+16), (x+9, y+h-4), 2)
        pygame.draw.rect(surface, TRASH_LITE,  (x, y, w, 14), 0, 3)
        pygame.draw.rect(surface, (200,200,200), (x+2, y+2, w-4, 5), 0, 2)
        pygame.draw.rect(surface, TRASH_DARK,  (x, y+10, w, 4), 0, 2)
        pygame.draw.rect(surface, TRASH_DARK,  (x+w//2-7, y-6, 14, 7), 0, 3)

    # ── SHOE ──────────────────────────────────────────────────────── #
    def _draw_shoe(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # sole
        pygame.draw.rect(surface, SHOE_SOLE, (x, y+h-10, w, 10), 0, 4)
        pygame.draw.rect(surface, (50, 30, 10), (x, y+h-10, w, 4), 0, 4)
        # upper body
        points = [(x+10, y+h-10), (x, y+h-24), (x+8, y+20),
                  (x+30, y+10), (x+w, y+20), (x+w, y+h-10)]
        pygame.draw.polygon(surface, SHOE_BODY, points)
        pygame.draw.polygon(surface, SHOE_LITE, [
            (x+10, y+h-10), (x+8, y+20), (x+14, y+14), (x+16, y+h-10)])
        # toe cap
        pygame.draw.ellipse(surface, SHOE_LITE, (x+w-30, y+16, 28, 20))
        # laces
        for i in range(3):
            ly = y + 26 + i * 10
            pygame.draw.line(surface, (200, 180, 160), (x+20, ly), (x+50, ly), 2)
            pygame.draw.line(surface, (200, 180, 160), (x+22+i*6, ly), (x+22+i*6, ly+8), 2)

    # ── VASE ──────────────────────────────────────────────────────── #
    def _draw_vase(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # body curved
        pygame.draw.polygon(surface, VASE_BODY, [
            (x+w//2-6, y), (x+w//2+6, y),
            (x+w-2, y+h//2), (x+w, y+h-8),
            (x, y+h-8), (x+2, y+h//2)])
        pygame.draw.polygon(surface, VASE_LITE, [
            (x+w//2-6, y), (x+w//2+4, y),
            (x+w//2+4, y+h//2), (x+w//2-6, y+h//2)])
        pygame.draw.polygon(surface, VASE_DARK, [
            (x+w-2, y+h//2), (x+w, y+h-8),
            (x+w-8, y+h-8), (x+w-6, y+h//2)])
        # neck
        pygame.draw.rect(surface, VASE_BODY, (x+w//2-8, y-10, 16, 14), 0, 3)
        pygame.draw.rect(surface, VASE_LITE, (x+w//2-8, y-10, 5, 14))
        # rim
        pygame.draw.rect(surface, VASE_DARK, (x+w//2-10, y-12, 20, 5), 0, 3)
        # base
        pygame.draw.rect(surface, VASE_DARK, (x+2, y+h-8, w-4, 8), 0, 2)
        # decorative lines
        pygame.draw.arc(surface, VASE_DARK,
                        (x+4, y+h//3, w-8, 20), 0, 3.14, 2)
        pygame.draw.arc(surface, VASE_DARK,
                        (x+6, y+h//2, w-12, 16), 0, 3.14, 2)
        # flowers sticking out
        for i, fx in enumerate([x+w//2-8, x+w//2+2]):
            fh = 24 + i * 8
            pygame.draw.line(surface, FLOWER_STEM, (fx, y-10), (fx + i*6, y-10-fh), 2)
            pygame.draw.circle(surface, FLOWER_PET, (fx + i*6, y-10-fh), 7)
            pygame.draw.circle(surface, FLOWER_CEN, (fx + i*6, y-10-fh), 3)

    # ── BROOM ─────────────────────────────────────────────────────── #
    def _draw_broom(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # stick leaning slightly
        cx = x + w // 2
        pygame.draw.line(surface, BROOM_STICK, (cx+4, y), (cx, y+h-24), 5)
        pygame.draw.line(surface, (200, 140, 60), (cx+5, y), (cx+5, y+h-24), 1)
        # head at bottom
        pygame.draw.rect(surface, BROOM_HEAD, (x, y+h-28, w, 28), 0, 3)
        pygame.draw.rect(surface, (220, 180, 100), (x, y+h-28, w, 6))
        pygame.draw.rect(surface, BROOM_DARK, (x, y+h-22, w, 4))
        # bristles
        for i in range(7):
            bx = x + 2 + i * 4
            pygame.draw.line(surface, BROOM_DARK,
                             (bx, y+h-18), (bx + (i%2)*2, y+h), 2)
        # binding
        pygame.draw.rect(surface, (160, 100, 30), (x+2, y+h-30, w-4, 5), 0, 2)

    # ── FLOWER POT ────────────────────────────────────────────────── #
    def _draw_flower_pot(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        pot_y = y + h - 44
        # pot body
        pygame.draw.polygon(surface, POT_BODY, [
            (x+6, pot_y), (x+w-6, pot_y),
            (x+w, pot_y+38), (x, pot_y+38)])
        pygame.draw.polygon(surface, (210, 110, 65), [
            (x+6, pot_y), (x+16, pot_y),
            (x+18, pot_y+38), (x, pot_y+38)])
        pygame.draw.polygon(surface, POT_DARK, [
            (x+w-8, pot_y), (x+w-6, pot_y),
            (x+w, pot_y+38), (x+w-10, pot_y+38)])
        pygame.draw.rect(surface, POT_DARK, (x, pot_y+34, w, 4))
        # pot rim
        pygame.draw.rect(surface, POT_DARK, (x+2, pot_y-6, w-4, 8), 0, 3)
        pygame.draw.rect(surface, (210, 110, 65), (x+2, pot_y-6, w-4, 4), 0, 3)
        # soil
        pygame.draw.ellipse(surface, (80, 50, 20), (x+4, pot_y-4, w-8, 8))
        # plant stems
        for i, (sx, angle) in enumerate([(x+w//2-6, -70), (x+w//2, -90), (x+w//2+6, -110)]):
            import math
            rad = math.radians(angle)
            length = 30 + i * 8
            ex = int(sx + math.cos(rad) * length)
            ey = int(pot_y - 4 + math.sin(rad) * length)
            pygame.draw.line(surface, PLANT_GREEN, (sx, pot_y-4), (ex, ey), 3)
            pygame.draw.circle(surface, PLANT_DARK, (ex, ey), 7)
            pygame.draw.circle(surface, PLANT_GREEN, (ex, ey), 5)

    # ── SOFA ──────────────────────────────────────────────────────── #
    def _draw_sofa(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # base/seat
        pygame.draw.rect(surface, SOFA_DARK,  (x+10, y+44, w-20, h-44), 0, 4)
        pygame.draw.rect(surface, SOFA_BODY,  (x+10, y+44, w-20, h-54), 0, 4)
        pygame.draw.rect(surface, SOFA_LITE,  (x+10, y+44, w-20, 8), 0, 4)
        # legs
        for lx in [x+14, x+w-22]:
            pygame.draw.rect(surface, CHAIR_DARK, (lx, y+h-10, 10, 10), 0, 2)
        # backrest
        pygame.draw.rect(surface, SOFA_DARK,  (x+4,  y+12, w-8, 36), 0, 4)
        pygame.draw.rect(surface, SOFA_BODY,  (x+4,  y+8,  w-8, 36), 0, 4)
        pygame.draw.rect(surface, SOFA_LITE,  (x+4,  y+8,  w-8, 10), 0, 4)
        # arm rests
        for ax in [x, x+w-22]:
            pygame.draw.rect(surface, SOFA_DARK, (ax, y+22, 22, h-32), 0, 4)
            pygame.draw.rect(surface, SOFA_BODY, (ax, y+18, 22, h-36), 0, 4)
            pygame.draw.rect(surface, SOFA_LITE, (ax, y+18, 22, 8),    0, 4)
        # cushion divisions
        mid = x + w // 2
        pygame.draw.line(surface, SOFA_DARK, (mid, y+44), (mid, y+h-10), 3)
        # pillows
        for px2 in [x+28, x+w-68]:
            pygame.draw.rect(surface, SOFA_PILLOW, (px2, y+12, 34, 30), 0, 4)
            pygame.draw.rect(surface, (240, 210, 255), (px2, y+12, 34, 8), 0, 4)
            pygame.draw.line(surface, SOFA_BODY, (px2+17, y+14), (px2+17, y+38), 2)


class Platform:
    def __init__(self, x, ground_y, kind=None):
        self.ground_y  = ground_y
        self.kind      = kind or random.choice(["table", "chair"])
        self._setup(x)

    def _setup(self, x):
        if self.kind == "table":
            self.rect      = pygame.Rect(x, self.ground_y - 130, 160, 14)
            self.full_rect = pygame.Rect(x, self.ground_y - 130, 160, 130)
        else:
            self.rect      = pygame.Rect(x, self.ground_y - 88, 80, 12)
            self.full_rect = pygame.Rect(x, self.ground_y - 88, 80, 88)

    def update(self, scroll_speed):
        self.rect.x      -= scroll_speed
        self.full_rect.x -= scroll_speed
        return self.rect.right > 0

    def is_springboard(self):
        return self.kind == "table"

    def draw(self, surface):
        if self.kind == "table":
            self._draw_table(surface)
        else:
            self._draw_chair(surface)

    def _draw_table(self, surface):
        x, y = self.rect.x, self.rect.y
        w    = self.rect.width
        pygame.draw.rect(surface, TABLE_TOP,  (x, y, w, 14), 0, 2)
        pygame.draw.rect(surface, TABLE_LITE, (x, y, w, 5))
        pygame.draw.rect(surface, TABLE_LITE, (x, y, 4, 14))
        pygame.draw.rect(surface, TABLE_DARK, (x, y+10, w, 4))
        lh = self.ground_y - y - 14
        for lx in [x+8, x+w-18]:
            pygame.draw.rect(surface, TABLE_TOP,  (lx, y+14, 12, lh))
            pygame.draw.rect(surface, TABLE_LITE, (lx, y+14, 3,  lh))
            pygame.draw.rect(surface, TABLE_DARK, (lx+9, y+14, 3, lh))

    def _draw_chair(self, surface):
        x, y = self.rect.x, self.rect.y
        w    = self.rect.width
        pygame.draw.rect(surface, CHAIR_SEAT, (x, y, w, 12), 0, 2)
        pygame.draw.rect(surface, CHAIR_WOOD, (x, y, w, 4))
        pygame.draw.rect(surface, CHAIR_DARK, (x, y+8, w, 4))
        pygame.draw.rect(surface, CHAIR_WOOD, (x+w-14, y-46, 12, 48), 0, 2)
        pygame.draw.rect(surface, CHAIR_WOOD, (x+w-14, y-44, 12, 9),  0, 2)
        lh = self.ground_y - y - 12
        for lx in [x+5, x+w-14]:
            pygame.draw.rect(surface, CHAIR_WOOD, (lx, y+12, 9, lh))
            pygame.draw.rect(surface, CHAIR_DARK, (lx+6, y+12, 3, lh))


class Cheese:
    SIZE = 26

    def __init__(self, x, y):
        self.rect      = pygame.Rect(x, y, self.SIZE, self.SIZE)
        self.collected = False
        self.bob_timer = random.randint(0, 60)

    def update(self, scroll_speed):
        self.rect.x    -= scroll_speed
        self.bob_timer += 1
        self.rect.y    += int(pygame.math.Vector2(0, 1).rotate(self.bob_timer * 6).y)
        return self.rect.right > 0 and not self.collected

    def draw(self, surface):
        if self.collected:
            return
        x, y = self.rect.x, self.rect.y
        s    = self.SIZE
        pygame.draw.polygon(surface, CHEESE_YEL,
                            [(x, y+s), (x+s, y+s), (x+s, y+6), (x+s//2, y)])
        pygame.draw.polygon(surface, CHEESE_LITE,
                            [(x, y+s), (x+s//2, y), (x+s//2, y-4), (x, y+s-4)])
        pygame.draw.polygon(surface, CHEESE_DARK,
                            [(x+s, y+s), (x+s, y+6), (x+s+5, y+10), (x+s+5, y+s)])
        pygame.draw.rect(surface, CHEESE_DARK, (x, y+s-4, s, 4))
        pygame.draw.ellipse(surface, CHEESE_HOLE, (x+5,  y+s-16, 8,  6))
        pygame.draw.ellipse(surface, CHEESE_HOLE, (x+14, y+s-12, 10, 7))
        pygame.draw.ellipse(surface, CHEESE_HOLE, (x+8,  y+s-6,  6,  4))
        pygame.draw.rect(surface, (255, 240, 130), (x+3, y+s-18, 4, 3))
        pygame.draw.rect(surface, (255, 240, 130), (x+3, y+s-20, 8, 2))


class ObstacleManager:
    def __init__(self, width, ground_y):
        self.width         = width
        self.ground_y      = ground_y
        self.obstacles     = []
        self.platforms     = []
        self.cheeses       = []
        self.spawn_timer   = 0
        self.cheese_timer  = 0
        self.next_spawn_in = 90

    def update(self, scroll_speed):
        self.obstacles = [o for o in self.obstacles if o.update(scroll_speed)]
        self.platforms = [p for p in self.platforms if p.update(scroll_speed)]
        self.cheeses   = [c for c in self.cheeses   if c.update(scroll_speed)]

        self.spawn_timer += 1
        if self.spawn_timer >= self.next_spawn_in:
            self._spawn_next()
            self.spawn_timer   = 0
            self.next_spawn_in = random.randint(55, 130)

        self.cheese_timer += 1
        if self.cheese_timer >= random.randint(160, 280):
            self._spawn_cheese()
            self.cheese_timer = 0

    def _spawn_next(self):
        x = self.width + 50
        if random.random() < 0.45:
            self.platforms.append(Platform(x, self.ground_y))
            if random.random() < 0.6:
                p = self.platforms[-1]
                self.cheeses.append(Cheese(p.rect.x + p.rect.width // 2,
                                           p.rect.y - 34))
        else:
            self.obstacles.append(Obstacle(x, self.ground_y))

    def _spawn_cheese(self):
        x = self.width + 80
        y = random.randint(self.ground_y - 170, self.ground_y - 60)
        self.cheeses.append(Cheese(x, y))

    def check_cheese_collision(self, player_rect):
        for cheese in self.cheeses:
            if not cheese.collected and player_rect.colliderect(cheese.rect):
                cheese.collected = True
                return True
        return False

    def check_obstacle_collision(self, player):
        if player.is_dashing:
            return False
        for obs in self.obstacles:
            if player.rect.colliderect(obs.rect):
                return True
        return False

    def check_platform_collision(self, player):
        for plat in self.platforms:
            if player.rect.colliderect(plat.rect):
                if player.vel_y > 0 and player.rect.bottom < plat.rect.bottom + 12:
                    player.rect.bottom = plat.rect.top
                    player.vel_y       = 0
                    player.is_grounded = True
                    pass

    def draw(self, surface):
        for o in self.obstacles:
            o.draw(surface)
        for p in self.platforms:
            p.draw(surface)
        for c in self.cheeses:
            c.draw(surface)# obstacles.py
import pygame
import random

# Colors
TRASH_BODY  = (85,  85,  85)
TRASH_LITE  = (119, 119, 119)
TRASH_DARK  = (51,  51,  51)
CHAIR_WOOD  = (139, 90,  43)
CHAIR_SEAT  = (170, 112, 48)
CHAIR_DARK  = (92,  58,  16)
TABLE_TOP   = (139, 90,  43)
TABLE_LITE  = (170, 112, 48)
TABLE_DARK  = (92,  58,  16)
CHEESE_YEL  = (245, 200, 0)
CHEESE_LITE = (255, 224, 51)
CHEESE_DARK = (196, 154, 0)
CHEESE_HOLE = (184, 136, 0)
SOFA_BODY   = (100, 60,  140)
SOFA_LITE   = (130, 85,  170)
SOFA_DARK   = (70,  35,  100)
SOFA_PILLOW = (220, 180, 255)
SHOE_BODY   = (60,  35,  15)
SHOE_SOLE   = (30,  20,  8)
SHOE_LITE   = (90,  55,  25)
VASE_BODY   = (200, 80,  40)
VASE_LITE   = (230, 110, 60)
VASE_DARK   = (150, 50,  20)
VASE_WATER  = (100, 180, 220)
FLOWER_STEM = (50,  130, 50)
FLOWER_PET  = (240, 80,  120)
FLOWER_CEN  = (255, 220, 50)
BROOM_STICK = (160, 100, 40)
BROOM_HEAD  = (200, 160, 80)
BROOM_DARK  = (140, 100, 40)
POT_BODY    = (180, 90,  50)
POT_DARK    = (130, 60,  30)
PLANT_GREEN = (50,  160, 50)
PLANT_DARK  = (30,  110, 30)


class Obstacle:
    KINDS = ["trashcan", "shoe", "vase", "broom", "flower_pot", "sofa"]

    def __init__(self, x, ground_y, kind=None):
        self.ground_y = ground_y
        self.kind     = kind or random.choice(self.KINDS)
        self._setup(x)

    def _setup(self, x):
        sizes = {
            "trashcan":   (46, 60),
            "shoe":       (80, 50),
            "vase":       (44, 72),
            "broom":      (28, 110),
            "flower_pot": (50, 80),
            "sofa":       (160, 90),
        }
        w, h = sizes[self.kind]
        self.rect = pygame.Rect(x, self.ground_y - h, w, h)

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        return self.rect.right > 0

    def draw(self, surface):
        getattr(self, f"_draw_{self.kind}")(surface)

    # ── TRASHCAN ──────────────────────────────────────────────────── #
    def _draw_trashcan(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        pygame.draw.rect(surface, TRASH_BODY,  (x+3, y+12, w-6, h-12), 0, 3)
        pygame.draw.rect(surface, TRASH_LITE,  (x+3, y+12, 5, h-12))
        pygame.draw.rect(surface, TRASH_LITE,  (x+3, y+12, w-6, 4))
        pygame.draw.rect(surface, TRASH_DARK,  (x+w-6, y+12, 5, h-12))
        for by in [y+26, y+42]:
            pygame.draw.rect(surface, TRASH_DARK, (x+3, by, w-6, 3))
        pygame.draw.line(surface, TRASH_LITE, (x+9, y+16), (x+9, y+h-4), 2)
        pygame.draw.rect(surface, TRASH_LITE,  (x, y, w, 14), 0, 3)
        pygame.draw.rect(surface, (200,200,200), (x+2, y+2, w-4, 5), 0, 2)
        pygame.draw.rect(surface, TRASH_DARK,  (x, y+10, w, 4), 0, 2)
        pygame.draw.rect(surface, TRASH_DARK,  (x+w//2-7, y-6, 14, 7), 0, 3)

    # ── SHOE ──────────────────────────────────────────────────────── #
    def _draw_shoe(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # sole
        pygame.draw.rect(surface, SHOE_SOLE, (x, y+h-10, w, 10), 0, 4)
        pygame.draw.rect(surface, (50, 30, 10), (x, y+h-10, w, 4), 0, 4)
        # upper body
        points = [(x+10, y+h-10), (x, y+h-24), (x+8, y+20),
                  (x+30, y+10), (x+w, y+20), (x+w, y+h-10)]
        pygame.draw.polygon(surface, SHOE_BODY, points)
        pygame.draw.polygon(surface, SHOE_LITE, [
            (x+10, y+h-10), (x+8, y+20), (x+14, y+14), (x+16, y+h-10)])
        # toe cap
        pygame.draw.ellipse(surface, SHOE_LITE, (x+w-30, y+16, 28, 20))
        # laces
        for i in range(3):
            ly = y + 26 + i * 10
            pygame.draw.line(surface, (200, 180, 160), (x+20, ly), (x+50, ly), 2)
            pygame.draw.line(surface, (200, 180, 160), (x+22+i*6, ly), (x+22+i*6, ly+8), 2)

    # ── VASE ──────────────────────────────────────────────────────── #
    def _draw_vase(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # body curved
        pygame.draw.polygon(surface, VASE_BODY, [
            (x+w//2-6, y), (x+w//2+6, y),
            (x+w-2, y+h//2), (x+w, y+h-8),
            (x, y+h-8), (x+2, y+h//2)])
        pygame.draw.polygon(surface, VASE_LITE, [
            (x+w//2-6, y), (x+w//2+4, y),
            (x+w//2+4, y+h//2), (x+w//2-6, y+h//2)])
        pygame.draw.polygon(surface, VASE_DARK, [
            (x+w-2, y+h//2), (x+w, y+h-8),
            (x+w-8, y+h-8), (x+w-6, y+h//2)])
        # neck
        pygame.draw.rect(surface, VASE_BODY, (x+w//2-8, y-10, 16, 14), 0, 3)
        pygame.draw.rect(surface, VASE_LITE, (x+w//2-8, y-10, 5, 14))
        # rim
        pygame.draw.rect(surface, VASE_DARK, (x+w//2-10, y-12, 20, 5), 0, 3)
        # base
        pygame.draw.rect(surface, VASE_DARK, (x+2, y+h-8, w-4, 8), 0, 2)
        # decorative lines
        pygame.draw.arc(surface, VASE_DARK,
                        (x+4, y+h//3, w-8, 20), 0, 3.14, 2)
        pygame.draw.arc(surface, VASE_DARK,
                        (x+6, y+h//2, w-12, 16), 0, 3.14, 2)
        # flowers sticking out
        for i, fx in enumerate([x+w//2-8, x+w//2+2]):
            fh = 24 + i * 8
            pygame.draw.line(surface, FLOWER_STEM, (fx, y-10), (fx + i*6, y-10-fh), 2)
            pygame.draw.circle(surface, FLOWER_PET, (fx + i*6, y-10-fh), 7)
            pygame.draw.circle(surface, FLOWER_CEN, (fx + i*6, y-10-fh), 3)

    # ── BROOM ─────────────────────────────────────────────────────── #
    def _draw_broom(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # stick leaning slightly
        cx = x + w // 2
        pygame.draw.line(surface, BROOM_STICK, (cx+4, y), (cx, y+h-24), 5)
        pygame.draw.line(surface, (200, 140, 60), (cx+5, y), (cx+5, y+h-24), 1)
        # head at bottom
        pygame.draw.rect(surface, BROOM_HEAD, (x, y+h-28, w, 28), 0, 3)
        pygame.draw.rect(surface, (220, 180, 100), (x, y+h-28, w, 6))
        pygame.draw.rect(surface, BROOM_DARK, (x, y+h-22, w, 4))
        # bristles
        for i in range(7):
            bx = x + 2 + i * 4
            pygame.draw.line(surface, BROOM_DARK,
                             (bx, y+h-18), (bx + (i%2)*2, y+h), 2)
        # binding
        pygame.draw.rect(surface, (160, 100, 30), (x+2, y+h-30, w-4, 5), 0, 2)

    # ── FLOWER POT ────────────────────────────────────────────────── #
    def _draw_flower_pot(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        pot_y = y + h - 44
        # pot body
        pygame.draw.polygon(surface, POT_BODY, [
            (x+6, pot_y), (x+w-6, pot_y),
            (x+w, pot_y+38), (x, pot_y+38)])
        pygame.draw.polygon(surface, (210, 110, 65), [
            (x+6, pot_y), (x+16, pot_y),
            (x+18, pot_y+38), (x, pot_y+38)])
        pygame.draw.polygon(surface, POT_DARK, [
            (x+w-8, pot_y), (x+w-6, pot_y),
            (x+w, pot_y+38), (x+w-10, pot_y+38)])
        pygame.draw.rect(surface, POT_DARK, (x, pot_y+34, w, 4))
        # pot rim
        pygame.draw.rect(surface, POT_DARK, (x+2, pot_y-6, w-4, 8), 0, 3)
        pygame.draw.rect(surface, (210, 110, 65), (x+2, pot_y-6, w-4, 4), 0, 3)
        # soil
        pygame.draw.ellipse(surface, (80, 50, 20), (x+4, pot_y-4, w-8, 8))
        # plant stems
        for i, (sx, angle) in enumerate([(x+w//2-6, -70), (x+w//2, -90), (x+w//2+6, -110)]):
            import math
            rad = math.radians(angle)
            length = 30 + i * 8
            ex = int(sx + math.cos(rad) * length)
            ey = int(pot_y - 4 + math.sin(rad) * length)
            pygame.draw.line(surface, PLANT_GREEN, (sx, pot_y-4), (ex, ey), 3)
            pygame.draw.circle(surface, PLANT_DARK, (ex, ey), 7)
            pygame.draw.circle(surface, PLANT_GREEN, (ex, ey), 5)

    # ── SOFA ──────────────────────────────────────────────────────── #
    def _draw_sofa(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # base/seat
        pygame.draw.rect(surface, SOFA_DARK,  (x+10, y+44, w-20, h-44), 0, 4)
        pygame.draw.rect(surface, SOFA_BODY,  (x+10, y+44, w-20, h-54), 0, 4)
        pygame.draw.rect(surface, SOFA_LITE,  (x+10, y+44, w-20, 8), 0, 4)
        # legs
        for lx in [x+14, x+w-22]:
            pygame.draw.rect(surface, CHAIR_DARK, (lx, y+h-10, 10, 10), 0, 2)
        # backrest
        pygame.draw.rect(surface, SOFA_DARK,  (x+4,  y+12, w-8, 36), 0, 4)
        pygame.draw.rect(surface, SOFA_BODY,  (x+4,  y+8,  w-8, 36), 0, 4)
        pygame.draw.rect(surface, SOFA_LITE,  (x+4,  y+8,  w-8, 10), 0, 4)
        # arm rests
        for ax in [x, x+w-22]:
            pygame.draw.rect(surface, SOFA_DARK, (ax, y+22, 22, h-32), 0, 4)
            pygame.draw.rect(surface, SOFA_BODY, (ax, y+18, 22, h-36), 0, 4)
            pygame.draw.rect(surface, SOFA_LITE, (ax, y+18, 22, 8),    0, 4)
        # cushion divisions
        mid = x + w // 2
        pygame.draw.line(surface, SOFA_DARK, (mid, y+44), (mid, y+h-10), 3)
        # pillows
        for px2 in [x+28, x+w-68]:
            pygame.draw.rect(surface, SOFA_PILLOW, (px2, y+12, 34, 30), 0, 4)
            pygame.draw.rect(surface, (240, 210, 255), (px2, y+12, 34, 8), 0, 4)
            pygame.draw.line(surface, SOFA_BODY, (px2+17, y+14), (px2+17, y+38), 2)


class Platform:
    def __init__(self, x, ground_y, kind=None):
        self.ground_y  = ground_y
        self.kind      = kind or random.choice(["table", "chair"])
        self._setup(x)

    def _setup(self, x):
        if self.kind == "table":
            self.rect      = pygame.Rect(x, self.ground_y - 130, 160, 14)
            self.full_rect = pygame.Rect(x, self.ground_y - 130, 160, 130)
        else:
            self.rect      = pygame.Rect(x, self.ground_y - 88, 80, 12)
            self.full_rect = pygame.Rect(x, self.ground_y - 88, 80, 88)

    def update(self, scroll_speed):
        self.rect.x      -= scroll_speed
        self.full_rect.x -= scroll_speed
        return self.rect.right > 0

    def is_springboard(self):
        return self.kind == "table"

    def draw(self, surface):
        if self.kind == "table":
            self._draw_table(surface)
        else:
            self._draw_chair(surface)

    def _draw_table(self, surface):
        x, y = self.rect.x, self.rect.y
        w    = self.rect.width
        pygame.draw.rect(surface, TABLE_TOP,  (x, y, w, 14), 0, 2)
        pygame.draw.rect(surface, TABLE_LITE, (x, y, w, 5))
        pygame.draw.rect(surface, TABLE_LITE, (x, y, 4, 14))
        pygame.draw.rect(surface, TABLE_DARK, (x, y+10, w, 4))
        lh = self.ground_y - y - 14
        for lx in [x+8, x+w-18]:
            pygame.draw.rect(surface, TABLE_TOP,  (lx, y+14, 12, lh))
            pygame.draw.rect(surface, TABLE_LITE, (lx, y+14, 3,  lh))
            pygame.draw.rect(surface, TABLE_DARK, (lx+9, y+14, 3, lh))

    def _draw_chair(self, surface):
        x, y = self.rect.x, self.rect.y
        w    = self.rect.width
        pygame.draw.rect(surface, CHAIR_SEAT, (x, y, w, 12), 0, 2)
        pygame.draw.rect(surface, CHAIR_WOOD, (x, y, w, 4))
        pygame.draw.rect(surface, CHAIR_DARK, (x, y+8, w, 4))
        pygame.draw.rect(surface, CHAIR_WOOD, (x+w-14, y-46, 12, 48), 0, 2)
        pygame.draw.rect(surface, CHAIR_WOOD, (x+w-14, y-44, 12, 9),  0, 2)
        lh = self.ground_y - y - 12
        for lx in [x+5, x+w-14]:
            pygame.draw.rect(surface, CHAIR_WOOD, (lx, y+12, 9, lh))
            pygame.draw.rect(surface, CHAIR_DARK, (lx+6, y+12, 3, lh))


class Cheese:
    SIZE = 26

    def __init__(self, x, y):
        self.rect      = pygame.Rect(x, y, self.SIZE, self.SIZE)
        self.collected = False
        self.bob_timer = random.randint(0, 60)

    def update(self, scroll_speed):
        self.rect.x    -= scroll_speed
        self.bob_timer += 1
        self.rect.y    += int(pygame.math.Vector2(0, 1).rotate(self.bob_timer * 6).y)
        return self.rect.right > 0 and not self.collected

    def draw(self, surface):
        if self.collected:
            return
        x, y = self.rect.x, self.rect.y
        s    = self.SIZE
        pygame.draw.polygon(surface, CHEESE_YEL,
                            [(x, y+s), (x+s, y+s), (x+s, y+6), (x+s//2, y)])
        pygame.draw.polygon(surface, CHEESE_LITE,
                            [(x, y+s), (x+s//2, y), (x+s//2, y-4), (x, y+s-4)])
        pygame.draw.polygon(surface, CHEESE_DARK,
                            [(x+s, y+s), (x+s, y+6), (x+s+5, y+10), (x+s+5, y+s)])
        pygame.draw.rect(surface, CHEESE_DARK, (x, y+s-4, s, 4))
        pygame.draw.ellipse(surface, CHEESE_HOLE, (x+5,  y+s-16, 8,  6))
        pygame.draw.ellipse(surface, CHEESE_HOLE, (x+14, y+s-12, 10, 7))
        pygame.draw.ellipse(surface, CHEESE_HOLE, (x+8,  y+s-6,  6,  4))
        pygame.draw.rect(surface, (255, 240, 130), (x+3, y+s-18, 4, 3))
        pygame.draw.rect(surface, (255, 240, 130), (x+3, y+s-20, 8, 2))


class ObstacleManager:
    def __init__(self, width, ground_y):
        self.width         = width
        self.ground_y      = ground_y
        self.obstacles     = []
        self.platforms     = []
        self.cheeses       = []
        self.spawn_timer   = 0
        self.cheese_timer  = 0
        self.next_spawn_in = 90

    def update(self, scroll_speed):
        self.obstacles = [o for o in self.obstacles if o.update(scroll_speed)]
        self.platforms = [p for p in self.platforms if p.update(scroll_speed)]
        self.cheeses   = [c for c in self.cheeses   if c.update(scroll_speed)]

        self.spawn_timer += 1
        if self.spawn_timer >= self.next_spawn_in:
            self._spawn_next()
            self.spawn_timer   = 0
            self.next_spawn_in = random.randint(55, 130)

        self.cheese_timer += 1
        if self.cheese_timer >= random.randint(160, 280):
            self._spawn_cheese()
            self.cheese_timer = 0

    def _spawn_next(self):
        x = self.width + 50
        if random.random() < 0.45:
            self.platforms.append(Platform(x, self.ground_y))
            if random.random() < 0.6:
                p = self.platforms[-1]
                self.cheeses.append(Cheese(p.rect.x + p.rect.width // 2,
                                           p.rect.y - 34))
        else:
            self.obstacles.append(Obstacle(x, self.ground_y))

    def _spawn_cheese(self):
        x = self.width + 80
        y = random.randint(self.ground_y - 170, self.ground_y - 60)
        self.cheeses.append(Cheese(x, y))

    def check_cheese_collision(self, player_rect):
        for cheese in self.cheeses:
            if not cheese.collected and player_rect.colliderect(cheese.rect):
                cheese.collected = True
                return True
        return False

    def check_obstacle_collision(self, player):
        if player.is_dashing:
            return False
        for obs in self.obstacles:
            if player.rect.colliderect(obs.rect):
                return True
        return False

    def check_platform_collision(self, player):
        for plat in self.platforms:
            if player.rect.colliderect(plat.rect):
                if player.vel_y > 0 and player.rect.bottom < plat.rect.bottom + 12:
                    player.rect.bottom = plat.rect.top
                    player.vel_y       = 0
                    player.is_grounded = True
                    pass

    def draw(self, surface):
        for o in self.obstacles:
            o.draw(surface)
        for p in self.platforms:
            p.draw(surface)
        for c in self.cheeses:
            c.draw(surface)# obstacles.py
import pygame
import random

# Colors
TRASH_BODY  = (85,  85,  85)
TRASH_LITE  = (119, 119, 119)
TRASH_DARK  = (51,  51,  51)
CHAIR_WOOD  = (139, 90,  43)
CHAIR_SEAT  = (170, 112, 48)
CHAIR_DARK  = (92,  58,  16)
TABLE_TOP   = (139, 90,  43)
TABLE_LITE  = (170, 112, 48)
TABLE_DARK  = (92,  58,  16)
CHEESE_YEL  = (245, 200, 0)
CHEESE_LITE = (255, 224, 51)
CHEESE_DARK = (196, 154, 0)
CHEESE_HOLE = (184, 136, 0)
SOFA_BODY   = (100, 60,  140)
SOFA_LITE   = (130, 85,  170)
SOFA_DARK   = (70,  35,  100)
SOFA_PILLOW = (220, 180, 255)
SHOE_BODY   = (60,  35,  15)
SHOE_SOLE   = (30,  20,  8)
SHOE_LITE   = (90,  55,  25)
VASE_BODY   = (200, 80,  40)
VASE_LITE   = (230, 110, 60)
VASE_DARK   = (150, 50,  20)
VASE_WATER  = (100, 180, 220)
FLOWER_STEM = (50,  130, 50)
FLOWER_PET  = (240, 80,  120)
FLOWER_CEN  = (255, 220, 50)
BROOM_STICK = (160, 100, 40)
BROOM_HEAD  = (200, 160, 80)
BROOM_DARK  = (140, 100, 40)
POT_BODY    = (180, 90,  50)
POT_DARK    = (130, 60,  30)
PLANT_GREEN = (50,  160, 50)
PLANT_DARK  = (30,  110, 30)


class Obstacle:
    KINDS = ["trashcan", "shoe", "vase", "broom", "flower_pot", "sofa"]

    def __init__(self, x, ground_y, kind=None):
        self.ground_y = ground_y
        self.kind     = kind or random.choice(self.KINDS)
        self._setup(x)

    def _setup(self, x):
        sizes = {
            "trashcan":   (46, 60),
            "shoe":       (80, 50),
            "vase":       (44, 72),
            "broom":      (28, 110),
            "flower_pot": (50, 80),
            "sofa":       (160, 90),
        }
        w, h = sizes[self.kind]
        self.rect = pygame.Rect(x, self.ground_y - h, w, h)

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        return self.rect.right > 0

    def draw(self, surface):
        getattr(self, f"_draw_{self.kind}")(surface)

    # ── TRASHCAN ──────────────────────────────────────────────────── #
    def _draw_trashcan(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        pygame.draw.rect(surface, TRASH_BODY,  (x+3, y+12, w-6, h-12), 0, 3)
        pygame.draw.rect(surface, TRASH_LITE,  (x+3, y+12, 5, h-12))
        pygame.draw.rect(surface, TRASH_LITE,  (x+3, y+12, w-6, 4))
        pygame.draw.rect(surface, TRASH_DARK,  (x+w-6, y+12, 5, h-12))
        for by in [y+26, y+42]:
            pygame.draw.rect(surface, TRASH_DARK, (x+3, by, w-6, 3))
        pygame.draw.line(surface, TRASH_LITE, (x+9, y+16), (x+9, y+h-4), 2)
        pygame.draw.rect(surface, TRASH_LITE,  (x, y, w, 14), 0, 3)
        pygame.draw.rect(surface, (200,200,200), (x+2, y+2, w-4, 5), 0, 2)
        pygame.draw.rect(surface, TRASH_DARK,  (x, y+10, w, 4), 0, 2)
        pygame.draw.rect(surface, TRASH_DARK,  (x+w//2-7, y-6, 14, 7), 0, 3)

    # ── SHOE ──────────────────────────────────────────────────────── #
    def _draw_shoe(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # sole
        pygame.draw.rect(surface, SHOE_SOLE, (x, y+h-10, w, 10), 0, 4)
        pygame.draw.rect(surface, (50, 30, 10), (x, y+h-10, w, 4), 0, 4)
        # upper body
        points = [(x+10, y+h-10), (x, y+h-24), (x+8, y+20),
                  (x+30, y+10), (x+w, y+20), (x+w, y+h-10)]
        pygame.draw.polygon(surface, SHOE_BODY, points)
        pygame.draw.polygon(surface, SHOE_LITE, [
            (x+10, y+h-10), (x+8, y+20), (x+14, y+14), (x+16, y+h-10)])
        # toe cap
        pygame.draw.ellipse(surface, SHOE_LITE, (x+w-30, y+16, 28, 20))
        # laces
        for i in range(3):
            ly = y + 26 + i * 10
            pygame.draw.line(surface, (200, 180, 160), (x+20, ly), (x+50, ly), 2)
            pygame.draw.line(surface, (200, 180, 160), (x+22+i*6, ly), (x+22+i*6, ly+8), 2)

    # ── VASE ──────────────────────────────────────────────────────── #
    def _draw_vase(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # body curved
        pygame.draw.polygon(surface, VASE_BODY, [
            (x+w//2-6, y), (x+w//2+6, y),
            (x+w-2, y+h//2), (x+w, y+h-8),
            (x, y+h-8), (x+2, y+h//2)])
        pygame.draw.polygon(surface, VASE_LITE, [
            (x+w//2-6, y), (x+w//2+4, y),
            (x+w//2+4, y+h//2), (x+w//2-6, y+h//2)])
        pygame.draw.polygon(surface, VASE_DARK, [
            (x+w-2, y+h//2), (x+w, y+h-8),
            (x+w-8, y+h-8), (x+w-6, y+h//2)])
        # neck
        pygame.draw.rect(surface, VASE_BODY, (x+w//2-8, y-10, 16, 14), 0, 3)
        pygame.draw.rect(surface, VASE_LITE, (x+w//2-8, y-10, 5, 14))
        # rim
        pygame.draw.rect(surface, VASE_DARK, (x+w//2-10, y-12, 20, 5), 0, 3)
        # base
        pygame.draw.rect(surface, VASE_DARK, (x+2, y+h-8, w-4, 8), 0, 2)
        # decorative lines
        pygame.draw.arc(surface, VASE_DARK,
                        (x+4, y+h//3, w-8, 20), 0, 3.14, 2)
        pygame.draw.arc(surface, VASE_DARK,
                        (x+6, y+h//2, w-12, 16), 0, 3.14, 2)
        # flowers sticking out
        for i, fx in enumerate([x+w//2-8, x+w//2+2]):
            fh = 24 + i * 8
            pygame.draw.line(surface, FLOWER_STEM, (fx, y-10), (fx + i*6, y-10-fh), 2)
            pygame.draw.circle(surface, FLOWER_PET, (fx + i*6, y-10-fh), 7)
            pygame.draw.circle(surface, FLOWER_CEN, (fx + i*6, y-10-fh), 3)

    # ── BROOM ─────────────────────────────────────────────────────── #
    def _draw_broom(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # stick leaning slightly
        cx = x + w // 2
        pygame.draw.line(surface, BROOM_STICK, (cx+4, y), (cx, y+h-24), 5)
        pygame.draw.line(surface, (200, 140, 60), (cx+5, y), (cx+5, y+h-24), 1)
        # head at bottom
        pygame.draw.rect(surface, BROOM_HEAD, (x, y+h-28, w, 28), 0, 3)
        pygame.draw.rect(surface, (220, 180, 100), (x, y+h-28, w, 6))
        pygame.draw.rect(surface, BROOM_DARK, (x, y+h-22, w, 4))
        # bristles
        for i in range(7):
            bx = x + 2 + i * 4
            pygame.draw.line(surface, BROOM_DARK,
                             (bx, y+h-18), (bx + (i%2)*2, y+h), 2)
        # binding
        pygame.draw.rect(surface, (160, 100, 30), (x+2, y+h-30, w-4, 5), 0, 2)

    # ── FLOWER POT ────────────────────────────────────────────────── #
    def _draw_flower_pot(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        pot_y = y + h - 44
        # pot body
        pygame.draw.polygon(surface, POT_BODY, [
            (x+6, pot_y), (x+w-6, pot_y),
            (x+w, pot_y+38), (x, pot_y+38)])
        pygame.draw.polygon(surface, (210, 110, 65), [
            (x+6, pot_y), (x+16, pot_y),
            (x+18, pot_y+38), (x, pot_y+38)])
        pygame.draw.polygon(surface, POT_DARK, [
            (x+w-8, pot_y), (x+w-6, pot_y),
            (x+w, pot_y+38), (x+w-10, pot_y+38)])
        pygame.draw.rect(surface, POT_DARK, (x, pot_y+34, w, 4))
        # pot rim
        pygame.draw.rect(surface, POT_DARK, (x+2, pot_y-6, w-4, 8), 0, 3)
        pygame.draw.rect(surface, (210, 110, 65), (x+2, pot_y-6, w-4, 4), 0, 3)
        # soil
        pygame.draw.ellipse(surface, (80, 50, 20), (x+4, pot_y-4, w-8, 8))
        # plant stems
        for i, (sx, angle) in enumerate([(x+w//2-6, -70), (x+w//2, -90), (x+w//2+6, -110)]):
            import math
            rad = math.radians(angle)
            length = 30 + i * 8
            ex = int(sx + math.cos(rad) * length)
            ey = int(pot_y - 4 + math.sin(rad) * length)
            pygame.draw.line(surface, PLANT_GREEN, (sx, pot_y-4), (ex, ey), 3)
            pygame.draw.circle(surface, PLANT_DARK, (ex, ey), 7)
            pygame.draw.circle(surface, PLANT_GREEN, (ex, ey), 5)

    # ── SOFA ──────────────────────────────────────────────────────── #
    def _draw_sofa(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        # base/seat
        pygame.draw.rect(surface, SOFA_DARK,  (x+10, y+44, w-20, h-44), 0, 4)
        pygame.draw.rect(surface, SOFA_BODY,  (x+10, y+44, w-20, h-54), 0, 4)
        pygame.draw.rect(surface, SOFA_LITE,  (x+10, y+44, w-20, 8), 0, 4)
        # legs
        for lx in [x+14, x+w-22]:
            pygame.draw.rect(surface, CHAIR_DARK, (lx, y+h-10, 10, 10), 0, 2)
        # backrest
        pygame.draw.rect(surface, SOFA_DARK,  (x+4,  y+12, w-8, 36), 0, 4)
        pygame.draw.rect(surface, SOFA_BODY,  (x+4,  y+8,  w-8, 36), 0, 4)
        pygame.draw.rect(surface, SOFA_LITE,  (x+4,  y+8,  w-8, 10), 0, 4)
        # arm rests
        for ax in [x, x+w-22]:
            pygame.draw.rect(surface, SOFA_DARK, (ax, y+22, 22, h-32), 0, 4)
            pygame.draw.rect(surface, SOFA_BODY, (ax, y+18, 22, h-36), 0, 4)
            pygame.draw.rect(surface, SOFA_LITE, (ax, y+18, 22, 8),    0, 4)
        # cushion divisions
        mid = x + w // 2
        pygame.draw.line(surface, SOFA_DARK, (mid, y+44), (mid, y+h-10), 3)
        # pillows
        for px2 in [x+28, x+w-68]:
            pygame.draw.rect(surface, SOFA_PILLOW, (px2, y+12, 34, 30), 0, 4)
            pygame.draw.rect(surface, (240, 210, 255), (px2, y+12, 34, 8), 0, 4)
            pygame.draw.line(surface, SOFA_BODY, (px2+17, y+14), (px2+17, y+38), 2)


class Platform:
    def __init__(self, x, ground_y, kind=None):
        self.ground_y  = ground_y
        self.kind      = kind or random.choice(["table", "chair"])
        self._setup(x)

    def _setup(self, x):
        if self.kind == "table":
            self.rect      = pygame.Rect(x, self.ground_y - 130, 160, 14)
            self.full_rect = pygame.Rect(x, self.ground_y - 130, 160, 130)
        else:
            self.rect      = pygame.Rect(x, self.ground_y - 88, 80, 12)
            self.full_rect = pygame.Rect(x, self.ground_y - 88, 80, 88)

    def update(self, scroll_speed):
        self.rect.x      -= scroll_speed
        self.full_rect.x -= scroll_speed
        return self.rect.right > 0

    def is_springboard(self):
        return self.kind == "table"

    def draw(self, surface):
        if self.kind == "table":
            self._draw_table(surface)
        else:
            self._draw_chair(surface)

    def _draw_table(self, surface):
        x, y = self.rect.x, self.rect.y
        w    = self.rect.width
        pygame.draw.rect(surface, TABLE_TOP,  (x, y, w, 14), 0, 2)
        pygame.draw.rect(surface, TABLE_LITE, (x, y, w, 5))
        pygame.draw.rect(surface, TABLE_LITE, (x, y, 4, 14))
        pygame.draw.rect(surface, TABLE_DARK, (x, y+10, w, 4))
        lh = self.ground_y - y - 14
        for lx in [x+8, x+w-18]:
            pygame.draw.rect(surface, TABLE_TOP,  (lx, y+14, 12, lh))
            pygame.draw.rect(surface, TABLE_LITE, (lx, y+14, 3,  lh))
            pygame.draw.rect(surface, TABLE_DARK, (lx+9, y+14, 3, lh))

    def _draw_chair(self, surface):
        x, y = self.rect.x, self.rect.y
        w    = self.rect.width
        pygame.draw.rect(surface, CHAIR_SEAT, (x, y, w, 12), 0, 2)
        pygame.draw.rect(surface, CHAIR_WOOD, (x, y, w, 4))
        pygame.draw.rect(surface, CHAIR_DARK, (x, y+8, w, 4))
        pygame.draw.rect(surface, CHAIR_WOOD, (x+w-14, y-46, 12, 48), 0, 2)
        pygame.draw.rect(surface, CHAIR_WOOD, (x+w-14, y-44, 12, 9),  0, 2)
        lh = self.ground_y - y - 12
        for lx in [x+5, x+w-14]:
            pygame.draw.rect(surface, CHAIR_WOOD, (lx, y+12, 9, lh))
            pygame.draw.rect(surface, CHAIR_DARK, (lx+6, y+12, 3, lh))


class Cheese:
    SIZE = 26

    def __init__(self, x, y):
        self.rect      = pygame.Rect(x, y, self.SIZE, self.SIZE)
        self.collected = False
        self.bob_timer = random.randint(0, 60)

    def update(self, scroll_speed):
        self.rect.x    -= scroll_speed
        self.bob_timer += 1
        self.rect.y    += int(pygame.math.Vector2(0, 1).rotate(self.bob_timer * 6).y)
        return self.rect.right > 0 and not self.collected

    def draw(self, surface):
        if self.collected:
            return
        x, y = self.rect.x, self.rect.y
        s    = self.SIZE
        pygame.draw.polygon(surface, CHEESE_YEL,
                            [(x, y+s), (x+s, y+s), (x+s, y+6), (x+s//2, y)])
        pygame.draw.polygon(surface, CHEESE_LITE,
                            [(x, y+s), (x+s//2, y), (x+s//2, y-4), (x, y+s-4)])
        pygame.draw.polygon(surface, CHEESE_DARK,
                            [(x+s, y+s), (x+s, y+6), (x+s+5, y+10), (x+s+5, y+s)])
        pygame.draw.rect(surface, CHEESE_DARK, (x, y+s-4, s, 4))
        pygame.draw.ellipse(surface, CHEESE_HOLE, (x+5,  y+s-16, 8,  6))
        pygame.draw.ellipse(surface, CHEESE_HOLE, (x+14, y+s-12, 10, 7))
        pygame.draw.ellipse(surface, CHEESE_HOLE, (x+8,  y+s-6,  6,  4))
        pygame.draw.rect(surface, (255, 240, 130), (x+3, y+s-18, 4, 3))
        pygame.draw.rect(surface, (255, 240, 130), (x+3, y+s-20, 8, 2))


class ObstacleManager:
    def __init__(self, width, ground_y):
        self.width         = width
        self.ground_y      = ground_y
        self.obstacles     = []
        self.platforms     = []
        self.cheeses       = []
        self.spawn_timer   = 0
        self.cheese_timer  = 0
        self.next_spawn_in = 90

    def update(self, scroll_speed):
        self.obstacles = [o for o in self.obstacles if o.update(scroll_speed)]
        self.platforms = [p for p in self.platforms if p.update(scroll_speed)]
        self.cheeses   = [c for c in self.cheeses   if c.update(scroll_speed)]

        self.spawn_timer += 1
        if self.spawn_timer >= self.next_spawn_in:
            self._spawn_next()
            self.spawn_timer   = 0
            self.next_spawn_in = random.randint(55, 130)

        self.cheese_timer += 1
        if self.cheese_timer >= random.randint(160, 280):
            self._spawn_cheese()
            self.cheese_timer = 0

    def _spawn_next(self):
        x = self.width + 50
        if random.random() < 0.45:
            self.platforms.append(Platform(x, self.ground_y))
            if random.random() < 0.6:
                p = self.platforms[-1]
                self.cheeses.append(Cheese(p.rect.x + p.rect.width // 2,
                                           p.rect.y - 34))
        else:
            self.obstacles.append(Obstacle(x, self.ground_y))

    def _spawn_cheese(self):
        x = self.width + 80
        y = random.randint(self.ground_y - 170, self.ground_y - 60)
        self.cheeses.append(Cheese(x, y))

    def check_cheese_collision(self, player_rect):
        for cheese in self.cheeses:
            if not cheese.collected and player_rect.colliderect(cheese.rect):
                cheese.collected = True
                return True
        return False

    def check_obstacle_collision(self, player):
        if player.is_dashing:
            return False
        for obs in self.obstacles:
            if player.rect.colliderect(obs.rect):
                return True
        return False

    def check_platform_collision(self, player):
        for plat in self.platforms:
            if player.rect.colliderect(plat.rect):
                if player.vel_y > 0 and player.rect.bottom < plat.rect.bottom + 12:
                    player.rect.bottom = plat.rect.top
                    player.vel_y       = 0
                    player.is_grounded = True
                    pass

    def draw(self, surface):
        for o in self.obstacles:
            o.draw(surface)
        for p in self.platforms:
            p.draw(surface)
        for c in self.cheeses:
            c.draw(surface)