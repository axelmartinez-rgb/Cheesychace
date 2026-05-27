# main.py
# Mouse Escape: House Chase

import pygame
import random
import sys
import math

import background as bg
import characters as ch
import obstacles  as oc
import gravity    as gr
import movement   as mv

WIDTH, HEIGHT  = 800, 400
FPS            = 60
GROUND_Y       = HEIGHT - 50
SCROLL_SPEED   = 5

WHITE        = (255, 255, 255)
DARK         = (30,  20,  10)
GOLD         = (255, 200, 50)
RED          = (200, 50,  50)
DANGER_EMPTY = (60,  20,  20)
DANGER_FILL  = (220, 40,  40)
DANGER_FULL  = (255, 80,  80)


# ── Particles ─────────────────────────────────────────────────────── #
class Particle:
    def __init__(self, x, y, color):
        angle     = random.uniform(0, 2 * math.pi)
        speed     = random.uniform(2, 9)
        self.x    = float(x)
        self.y    = float(y)
        self.vx   = math.cos(angle) * speed
        self.vy   = math.sin(angle) * speed - 4
        self.life  = 1.0
        self.decay = random.uniform(0.04, 0.08)
        self.size  = random.randint(4, 10)
        self.color = color

    def update(self):
        self.x    += self.vx
        self.y    += self.vy
        self.vy   += 0.35
        self.life -= self.decay
        self.size  = max(1, self.size - 1)
        return self.life > 0

    def draw(self, surface):
        alpha = max(0, int(self.life * 255))
        s     = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
        surface.blit(s, (int(self.x) - self.size, int(self.y) - self.size))


def spawn_hit_particles(particles, x, y):
    """Stars burst when mouse hits an obstacle."""
    colors = [(255, 80, 80), (255, 180, 50), (255, 255, 100), (255, 255, 255)]
    for _ in range(22):
        particles.append(Particle(x, y, random.choice(colors)))


def spawn_catch_particles(particles, x, y):
    """Hearts/stars burst when cat catches mouse."""
    colors = [(255, 50, 50), (255, 100, 100), (255, 200, 200), (255, 80, 200)]
    for _ in range(30):
        particles.append(Particle(x, y, random.choice(colors)))


# ── Screens ───────────────────────────────────────────────────────── #
def draw_start_screen(surface, width, height):
    surface.fill((40, 25, 10))
    font_big = pygame.font.SysFont(None, 72)
    font_med = pygame.font.SysFont(None, 36)
    font_sm  = pygame.font.SysFont(None, 26)

    title = font_big.render("MOUSE ESCAPE",                        True, GOLD)
    sub   = font_med.render("House Chase",                         True, (220, 180, 100))
    hint  = font_sm.render("Press UP to start!",                   True, WHITE)
    tip1  = font_sm.render("↑ Arrow UP = Jump",                    True, (180, 180, 180))
    tip2  = font_sm.render("→ → Double RIGHT = DASH!",             True, (255, 220, 80))
    tip3  = font_sm.render("Collect cheese to fill the DASH bar!", True, (100, 220, 100))

    surface.blit(title, (width//2 - title.get_width()//2, 70))
    surface.blit(sub,   (width//2 - sub.get_width()//2,   148))
    surface.blit(hint,  (width//2 - hint.get_width()//2,  210))
    surface.blit(tip1,  (width//2 - tip1.get_width()//2,  258))
    surface.blit(tip2,  (width//2 - tip2.get_width()//2,  288))
    surface.blit(tip3,  (width//2 - tip3.get_width()//2,  318))

    pygame.draw.circle(surface, (160, 160, 160), (width//2, 48), 18)
    pygame.draw.circle(surface, (200, 140, 140), (width//2+12, 35), 8)
    pygame.draw.circle(surface, (30, 30, 30),    (width//2+10, 45), 3)


def draw_game_over(surface, width, height, score):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    font_big = pygame.font.SysFont(None, 80)
    font_med = pygame.font.SysFont(None, 40)
    font_sm  = pygame.font.SysFont(None, 28)

    go   = font_big.render("GAME OVER",            True, RED)
    sc   = font_med.render(f"Score: {score}",       True, GOLD)
    hint = font_sm.render("Press UP to play again", True, WHITE)

    surface.blit(go,   (width//2 - go.get_width()//2,   110))
    surface.blit(sc,   (width//2 - sc.get_width()//2,   210))
    surface.blit(hint, (width//2 - hint.get_width()//2, 275))


def draw_hud(surface, score):
    font = pygame.font.SysFont(None, 30)
    txt  = font.render(f"Score: {score}", True, DARK)
    surface.blit(txt, (WIDTH - 150, 12))


def draw_danger_bar(surface, danger):
    bx, by = 20, 34
    bw, bh = 160, 14
    pygame.draw.rect(surface, DANGER_EMPTY, (bx, by, bw, bh), 0, 4)
    fill_w = int(bw * danger / 100)
    if fill_w > 0:
        col = DANGER_FULL if danger > 80 else DANGER_FILL
        pygame.draw.rect(surface, col, (bx, by, fill_w, bh), 0, 4)
        if danger > 80 and pygame.time.get_ticks() % 300 < 150:
            pygame.draw.rect(surface, (255, 150, 150), (bx, by, fill_w, 5), 0, 4)
    pygame.draw.rect(surface, (180, 60, 60), (bx, by, bw, bh), 2, 4)
    font  = pygame.font.SysFont(None, 18)
    label = "!! RUN !!" if danger > 80 else "DANGER"
    txt   = font.render(label, True, (255, 160, 160))
    surface.blit(txt, (bx + bw + 6, by))


# ── Game over animations ───────────────────────────────────────────── #
def draw_caught_animation(surface, player, cat, timer):
    """Cat grabs mouse — shaking + cat jumps on top."""
    shake = int(math.sin(timer * 0.8) * 6) if timer < 90 else 0
    # draw cat lunging forward over mouse
    ox = int(math.sin(timer * 0.15) * 14) if timer < 60 else 14
    cat.rect.x += ox
    cat.draw(surface)
    cat.rect.x -= ox
    # draw mouse squished under cat
    mx = player.rect.x + shake
    my = player.rect.y + 8
    pygame.draw.ellipse(surface, (200, 200, 200), (mx, my + 10, 44, 14))  # flat body
    pygame.draw.ellipse(surface, (221, 221, 221), (mx + 4, my + 12, 36, 10))
    # stars around mouse
    for i in range(6):
        angle = timer * 0.12 + i * (math.pi / 3)
        sx = int(mx + 22 + math.cos(angle) * 28)
        sy = int(my + 8  + math.sin(angle) * 18)
        pygame.draw.circle(surface, (255, 220, 50), (sx, sy), 5)
        pygame.draw.circle(surface, (255, 255, 180), (sx, sy), 3)


def draw_hit_animation(surface, player, timer):
    """Mouse flashes and spins when hitting an obstacle."""
    if (timer // 6) % 2 == 0:   # flash every 6 frames
        return
    # draw mouse rotated/squished
    angle   = math.sin(timer * 0.5) * 30
    mx, my  = player.rect.centerx, player.rect.centery
    sq_surf = pygame.Surface((60, 40), pygame.SRCALPHA)
    pygame.draw.ellipse(sq_surf, (221, 221, 221, 200), (0, 8, 60, 24))
    pygame.draw.ellipse(sq_surf, (238, 238, 238, 200), (0, 8, 60, 12))
    rotated = pygame.transform.rotate(sq_surf, angle)
    surface.blit(rotated, (mx - rotated.get_width()//2,
                            my - rotated.get_height()//2))


# ── Reset ─────────────────────────────────────────────────────────── #
def reset_game():
    player   = ch.Mouse(GROUND_Y)
    cat      = ch.Cat(GROUND_Y)
    world_bg = bg.Background(WIDTH, HEIGHT, GROUND_Y)
    obs_mgr  = oc.ObstacleManager(WIDTH, GROUND_Y)
    return player, cat, world_bg, obs_mgr


# ── Main loop ─────────────────────────────────────────────────────── #
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mouse Escape: House Chase")
    clock  = pygame.time.Clock()

    STATE_START    = "start"
    STATE_RUNNING  = "running"
    STATE_HIT      = "hit"        # short animation then game over
    STATE_CAUGHT   = "caught"     # cat catches mouse animation
    STATE_GAMEOVER = "gameover"
    state = STATE_START

    player, cat, world_bg, obs_mgr = reset_game()
    score          = 0
    score_timer    = 0
    scroll_speed   = SCROLL_SPEED
    last_right_time = 0
    DOUBLE_TAP_MS  = 350

    # Danger / cat catch mechanic
    danger      = 0
    CAT_HOME_X  = 50
    CAT_CATCH_X = 280

    # Animation timers
    anim_timer  = 0
    particles   = []

    while True:
        now = pygame.time.get_ticks()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                key            = getattr(event, "key", None)
                mouse_button   = getattr(event, "button", None)  # 1=left, 2=middle, 3=right
                pressed_up     = (event.type == pygame.KEYDOWN and key == pygame.K_UP)
                pressed_right  = (event.type == pygame.KEYDOWN and key == pygame.K_RIGHT)
                pressed_click  = (event.type == pygame.MOUSEBUTTONDOWN)
                click_left     = (pressed_click and mouse_button == 1)
                click_right    = (pressed_click and mouse_button == 3)

                if state == STATE_START:
                    # any mouse click or UP starts the game
                    if pressed_up or pressed_click:
                        player.start()
                        state = STATE_RUNNING

                elif state == STATE_RUNNING:
                    # Left-click (mouse button 1) => jump
                    if pressed_up or click_left:
                        player.jump()
                    # Right-click (mouse button 3) => dash
                    if click_right:
                        player.activate_dash()
                    # Keep keyboard double-right for dash as before
                    if pressed_right:
                        if now - last_right_time <= DOUBLE_TAP_MS:
                            player.activate_dash()
                        last_right_time = now

                elif state == STATE_GAMEOVER:
                    if pressed_up or pressed_click:
                        player, cat, world_bg, obs_mgr = reset_game()
                        score          = 0
                        score_timer    = 0
                        scroll_speed   = SCROLL_SPEED
                        last_right_time = 0
                        danger         = 0
                        anim_timer     = 0
                        particles      = []
                        state          = STATE_RUNNING
                        player.start()

        # ── Update ── #
        if state == STATE_RUNNING:
            score_timer += 1
            if score_timer >= 30:
                score       += 1
                score_timer  = 0

            scroll_speed = SCROLL_SPEED + score // 10

            # Dashing: danger resets instantly, cat falls way behind
            if player.is_dashing:
                danger     = 0
                cat.rect.x = max(-80, cat.rect.x - 3)  # cat pushed back
            else:
                danger = min(100, danger + 0.14)

            # Cat speed depends on danger level
            # normal: slow creep. danger>80 (RUN): cat surges forward fast
            target_cat_x = CAT_HOME_X + int((CAT_CATCH_X - CAT_HOME_X) * danger / 100)
            if danger > 80:
                cat_speed = 2.2   # surging fast when RUN!
            elif danger > 50:
                cat_speed = 0.9   # medium speed
            else:
                cat_speed = 0.4   # slow creep

            if cat.rect.x < target_cat_x:
                cat.rect.x = min(cat.rect.x + cat_speed, target_cat_x)
            elif cat.rect.x > target_cat_x:
                cat.rect.x = max(cat.rect.x - 1.5, target_cat_x)
            # NOTE: danger bar never triggers game over on its own

            world_bg.update()
            gr.apply_gravity(player)
            player.update()
            obs_mgr.update(scroll_speed)
            obs_mgr.check_platform_collision(player)

            if obs_mgr.check_cheese_collision(player.rect):
                player.collect_cheese()

            # Obstacle hit — trigger hit animation
            if obs_mgr.check_obstacle_collision(player):
                spawn_hit_particles(particles,
                                    player.rect.centerx, player.rect.centery)
                anim_timer = 0
                state      = STATE_HIT

            # Cat catches mouse — trigger caught animation (only when cat physically reaches mouse)
            if cat.rect.right >= player.rect.left:
                spawn_catch_particles(particles,
                                      player.rect.centerx, player.rect.centery)
                anim_timer = 0
                state      = STATE_CAUGHT

            cat.update(player.is_dashing, scroll_speed)

        elif state == STATE_HIT:
            anim_timer += 1
            particles   = [p for p in particles if p.update()]
            if anim_timer >= 80:   # ~1.3 seconds then game over screen
                state = STATE_GAMEOVER

        elif state == STATE_CAUGHT:
            anim_timer += 1
            particles   = [p for p in particles if p.update()]
            if anim_timer >= 110:  # ~1.8 seconds then game over screen
                state = STATE_GAMEOVER

        # ── Draw ── #
        if state == STATE_START:
            draw_start_screen(screen, WIDTH, HEIGHT)

        else:
            world_bg.draw(screen)
            obs_mgr.draw(screen)

            if state == STATE_HIT:
                cat.draw(screen)
                for p in particles:
                    p.draw(screen)
                draw_hit_animation(screen, player, anim_timer)

            elif state == STATE_CAUGHT:
                for p in particles:
                    p.draw(screen)
                draw_caught_animation(screen, player, cat, anim_timer)

            else:
                cat.draw(screen)
                player.draw(screen)

            if state not in (STATE_HIT, STATE_CAUGHT):
                player.draw_cheese_bar(screen, WIDTH)
                draw_danger_bar(screen, danger)
                draw_hud(screen, score)

            if state == STATE_GAMEOVER:
                draw_game_over(screen, WIDTH, HEIGHT, score)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()