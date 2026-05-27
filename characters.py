# characters.py
import pygame
import math

# Mouse colors
MOUSE_BODY  = (221, 221, 221)
MOUSE_LIGHT = (238, 238, 238)
MOUSE_DARK  = (170, 170, 170)
MOUSE_EAR   = (255, 153, 153)
MOUSE_EYE   = (17,  17,  17)
MOUSE_NOSE  = (255, 136, 153)
MOUSE_TAIL  = (204, 204, 204)
MOUSE_DASH  = (255, 220, 50)

# Cat colors - orange tabby
CAT_BODY    = (221, 102, 0)
CAT_LIGHT   = (255, 136, 34)
CAT_DARK    = (170, 51,  0)
CAT_BELLY   = (255, 170, 102)
CAT_EAR     = (255, 153, 153)
CAT_EYE_R   = (255, 0,   0)
CAT_CLAW    = (255, 255, 204)
CAT_FANG    = (238, 238, 238)
CAT_NOSE    = (255, 68,  102)


class Mouse:
    def __init__(self, ground_y):
        self.ground_y    = ground_y
        self.rect        = pygame.Rect(300, ground_y - 35, 42, 28)
        self.vel_y       = 0
        self.vel_x       = 0
        self.gravity     = 0.5
        self.jump_force  = -15
        self.is_grounded = False

        self.cheese_bar  = 0
        self.is_dashing  = False
        self.dash_timer  = 0
        self.DASH_MAX    = 180

        self.waiting     = True
        self.frame       = 0
        self.frame_timer = 0

    def start(self):
        self.waiting = False

    def collect_cheese(self):
        self.cheese_bar = min(100, self.cheese_bar + 34)

    def activate_dash(self):
        if self.cheese_bar >= 100 and not self.is_dashing:
            self.is_dashing = True
            self.dash_timer = self.DASH_MAX
            self.cheese_bar = 0

    def jump(self):
        if self.is_grounded and not self.waiting:
            self.vel_y       = self.jump_force
            self.vel_x       = 8
            self.is_grounded = False

    def update(self):
        if self.waiting:
            return
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
        self.frame_timer += 1
        if self.frame_timer >= 8:
            self.frame       = (self.frame + 1) % 2
            self.frame_timer = 0

    def draw(self, surface):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        S = 2  # pixel size

        def px(rx, ry, rw, rh, color):
            pygame.draw.rect(surface, color,
                             (x + rx * S, y + ry * S, rw * S, rh * S))

        # dash glow
        if self.is_dashing:
            glow = pygame.Surface((w + 24, h + 24), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (255, 220, 50, 90), (0, 0, w + 24, h + 24))
            surface.blit(glow, (x - 12, y - 12))

        # tail
        leg_off = 2 if self.frame == 0 else -2
        pygame.draw.line(surface, MOUSE_TAIL,
                         (x, y + h // 2),
                         (x - 14, y + h // 2 + leg_off), 3)

        # body
        pygame.draw.rect(surface, MOUSE_BODY,  (x,     y + 4, w,     h - 4))
        pygame.draw.rect(surface, MOUSE_LIGHT, (x,     y + 4, 4,     h - 4))
        pygame.draw.rect(surface, MOUSE_LIGHT, (x,     y + 4, w,     4))
        pygame.draw.rect(surface, MOUSE_DARK,  (x + w - 4, y + 4, 4, h - 4))
        pygame.draw.rect(surface, MOUSE_DARK,  (x,     y + h - 4, w, 4))

        # head
        pygame.draw.rect(surface, MOUSE_BODY,  (x + w - 14, y,     26, 28))
        pygame.draw.rect(surface, MOUSE_LIGHT, (x + w - 14, y,     26, 4))
        pygame.draw.rect(surface, MOUSE_LIGHT, (x + w - 14, y,     4,  28))
        pygame.draw.rect(surface, MOUSE_DARK,  (x + w + 8,  y,     4,  28))
        pygame.draw.rect(surface, MOUSE_DARK,  (x + w - 14, y + 24, 26, 4))

        # ear
        pygame.draw.rect(surface, MOUSE_EAR,   (x + w + 4,  y - 8, 14, 14))
        pygame.draw.rect(surface, (255, 187, 187), (x + w + 6, y - 6, 8, 8))

        # eye
        pygame.draw.rect(surface, MOUSE_EYE,   (x + w + 2,  y + 6,  10, 10))
        pygame.draw.rect(surface, (51, 51, 51), (x + w + 4,  y + 8,  6,  6))
        pygame.draw.rect(surface, (255, 255, 255), (x + w + 2, y + 6, 4, 4))
        pygame.draw.rect(surface, (170, 170, 255), (x + w + 4, y + 8, 3, 3))

        # nose
        pygame.draw.rect(surface, MOUSE_NOSE,  (x + w + 12, y + 14, 8,  5))
        pygame.draw.rect(surface, (255, 187, 204), (x + w + 14, y + 15, 4, 2))

        # whiskers
        for i, wy in enumerate([y + 12, y + 16, y + 20]):
            pygame.draw.line(surface, (153, 153, 153),
                             (x + w + 18, wy), (x + w + 32, wy + i - 1), 1)

        # legs animated
        lo = 4 if self.frame == 0 else -4
        pygame.draw.rect(surface, MOUSE_BODY,  (x + 8,  y + h - 2, 8, 8 + lo))
        pygame.draw.rect(surface, MOUSE_DARK,  (x + 8,  y + h + 4 + lo, 10, 4))
        pygame.draw.rect(surface, MOUSE_BODY,  (x + 22, y + h - 2, 8, 8 - lo))
        pygame.draw.rect(surface, MOUSE_DARK,  (x + 22, y + h + 2 - lo, 10, 4))

        if self.waiting:
            font = pygame.font.SysFont(None, 22)
            txt  = font.render("Press SPACE to start!", True, (80, 40, 0))
            surface.blit(txt, (x - 30, y - 28))

    def draw_cheese_bar(self, surface, screen_width):
        bx, by = 20, 12
        bw, bh = 160, 16
        pygame.draw.rect(surface, (42, 21, 8),    (bx, by, bw, bh), 0, 4)
        fill_w = int(bw * self.cheese_bar / 100)
        if fill_w > 0:
            col = (255, 200, 0) if not self.is_dashing else (255, 120, 0)
            pygame.draw.rect(surface, col,         (bx, by, fill_w, bh), 0, 4)
            pygame.draw.rect(surface, (255, 238, 102), (bx, by, fill_w, 5), 0, 4)
        pygame.draw.rect(surface, (200, 150, 50), (bx, by, bw, bh), 2, 4)
        font  = pygame.font.SysFont(None, 18)
        label = "DASH!" if self.cheese_bar >= 100 else "CHEESE"
        txt   = font.render(label, True, (255, 240, 180))
        surface.blit(txt, (bx + bw + 6, by))


class Cat:
    def __init__(self, ground_y):
        self.ground_y    = ground_y
        self.rect        = pygame.Rect(18, ground_y - 112, 152, 112)
        self.frame       = 0
        self.frame_timer = 0
        self.snarl_timer = 0

    def update(self, mouse_is_dashing, scroll_speed):
        if mouse_is_dashing:
            if self.rect.x > -60:
                self.rect.x -= 2
        else:
            if self.rect.x < 18:
                self.rect.x += 1
        self.frame_timer += 1
        if self.frame_timer >= 7:
            self.frame       = (self.frame + 1) % 2
            self.frame_timer = 0
        self.snarl_timer = (self.snarl_timer + 1) % 60

    def draw(self, surface):
        x  = self.rect.x
        gy = self.ground_y
        S  = 1  # pixel scale

        def px(rx, ry, rw, rh, color):
            pygame.draw.rect(surface, color, (x + rx, gy - 112 + ry, rw, rh))

        # shadow
        shadow = pygame.Surface((160, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), (0, 0, 160, 8))
        surface.blit(shadow, (x + 4, gy - 6))

        # body
        px(18,  60, 148,  52, CAT_DARK)
        px(18,  56, 148,  52, CAT_BODY)
        px(18,  56, 148,   5, CAT_LIGHT)
        px(18,  56,   5,  52, CAT_LIGHT)
        px(161, 56,   5,  52, CAT_DARK)
        px(18, 103, 148,   5, CAT_DARK)
        # belly
        px(44,  68,  96,  36, (238, 136, 51))
        px(50,  74,  84,  28, CAT_BELLY)
        # stripes
        px(34,  56,   7,  52, CAT_DARK)
        px(66,  56,   5,  44, CAT_DARK)
        px(116, 56,   5,  44, CAT_DARK)
        px(148, 56,   7,  52, CAT_DARK)

        # neck
        px(56, 28,  72,  30, CAT_BODY)

        # head
        px(22,  0, 142, 100, CAT_DARK)
        px(22,  0, 142, 100, CAT_BODY)
        px(22,  0, 142,   5, CAT_LIGHT)
        px(22,  0,   5, 100, CAT_LIGHT)
        px(159, 0,   5, 100, CAT_DARK)
        px(22,  95, 142,  5, CAT_DARK)
        # chubby cheeks
        px(14, 36,  14,  40, (238, 119, 17))
        px(158,36,  14,  40, (204, 85,   0))
        # head stripes
        px(86,  0,   6,  30, CAT_DARK)
        px(60,  0,   5,  22, (187, 68, 0))
        px(118, 0,   5,  22, (187, 68, 0))

        # ears
        px(26, -36,  34,  40, CAT_BODY)
        px(20, -46,  22,  14, CAT_BODY)
        px(22, -56,  14,  12, CAT_BODY)
        px(28, -28,  20,  26, CAT_EAR)
        px(32, -24,  12,  16, (255, 187, 187))
        px(126,-36,  34,  40, CAT_BODY)
        px(144,-46,  22,  14, CAT_BODY)
        px(150,-56,  14,  12, CAT_BODY)
        px(132,-28,  20,  26, CAT_EAR)
        px(138,-24,  12,  16, (255, 187, 187))
        px(26, -36,  34,   4, CAT_DARK)
        px(126,-36,  34,   4, CAT_DARK)

        # eyes - big cartoon red
        px(30,  16,  50,  40, (51,   0,   0))
        px(106, 16,  50,  40, (51,   0,   0))
        px(34,  20,  42,  32, (255, 204, 204))
        px(110, 20,  42,  32, (255, 204, 204))
        px(38,  22,  34,  28, (255,   0,   0))
        px(114, 22,  34,  28, (255,   0,   0))
        px(42,  24,  26,  24, (255,  51,  51))
        px(118, 24,  26,  24, (255,  51,  51))
        # slit pupil
        px(52,  16,   6,  40, (17,    0,   0))
        px(128, 16,   6,  40, (17,    0,   0))
        # shine
        px(34,  22,   8,   8, (255, 255, 255))
        px(110, 22,   8,   8, (255, 255, 255))
        px(38,  26,   5,   5, (255, 170, 170))
        px(114, 26,   5,   5, (255, 170, 170))

        # brows angry
        px(24,   6,  58,   8, CAT_DARK)
        px(24,   4,   8,  16, (136, 34,   0))
        px(104,  6,  58,   8, CAT_DARK)
        px(154,  4,   8,  16, (136, 34,   0))

        # nose
        px(78,  62,  30,  14, (255, 68,  102))
        px(82,  64,  22,   8, (255, 102, 136))

        # mouth - snarl with two fangs
        px(48,  74,  90,   5, CAT_DARK)
        px(54,  79,  78,  18, (51,    0,   0))
        px(58,  81,  70,  14, (85,    0,   0))
        # two fangs
        px(58,  74,  12,  18, CAT_FANG)
        px(60,  74,   8,  18, (221, 221, 221))
        px(116, 74,  12,  18, CAT_FANG)
        px(118, 74,   8,  18, (221, 221, 221))
        px(54,  95,  78,   5, CAT_DARK)

        # whiskers
        for wx, length, sign in [(0, 22, -1), (168, 22, 1)]:
            for i, wy in enumerate([54, 62, 70]):
                pygame.draw.line(surface, (255, 238, 204),
                                 (x + wx, gy - 112 + wy),
                                 (x + wx + sign * length, gy - 112 + wy + (i-1)), 1)

        # legs animated
        lo = 6 if self.frame == 0 else -6
        for i, lx in enumerate([24, 58, 100, 134]):
            pygame.draw.rect(surface, CAT_BODY,
                             (x + lx, gy - 8, 24, 14))
            off = lo if i % 2 == 0 else -lo
            pygame.draw.rect(surface, CAT_BODY,
                             (x + lx, gy + 4, 24, 6 + abs(off) // 2))

        # claws
        px(18, 104, 148,   6, CAT_BODY)
        for cx in [28, 42, 62, 76, 104, 118, 138, 152]:
            px(cx, 108,   6,  10, CAT_CLAW)

        # tail
        tail_wave = 10 if self.frame == 0 else -10
        pygame.draw.arc(surface, CAT_BODY,
                        (x - 24, gy - 112 + 50, 44, 44), 0, math.pi, 5)
        pygame.draw.circle(surface, (238, 119, 17),
                           (x - 20, gy - 112 + 46 + tail_wave // 2), 8)