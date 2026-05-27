# gravity.py
# Handles gravity and vertical physics for the player

GROUND_Y       = 350   # Must match main.py (HEIGHT - 50)
NORMAL_GRAVITY = 0.5
GLIDE_GRAVITY  = 0.25  # Slower fall when holding jump


def apply_gravity(player, is_jumping_held=False):
    """Apply gravity and move the player each frame."""
    if not player.is_grounded:
        if player.vel_y > 0 and is_jumping_held:
            player.vel_y += GLIDE_GRAVITY
        else:
            player.vel_y += NORMAL_GRAVITY

    # Move player vertically
    player.rect.y += player.vel_y

    # Apply horizontal jump boost and decay it back to 0
    if player.vel_x > 0:
        player.rect.x += player.vel_x
        player.vel_x  = max(0, player.vel_x - 0.4)  # smoothly slow down

    # Once landed, snap back to fixed x position
    if player.is_grounded and player.vel_x == 0:
        if player.rect.x > 300:
            player.rect.x -= 3
        elif player.rect.x < 300:
            player.rect.x = 300

    # Floor collision
    if player.rect.bottom >= GROUND_Y:
        player.rect.bottom = GROUND_Y
        player.vel_y       = 0
        player.is_grounded = True
    else:
        player.is_grounded = False


def apply_dive(player):
    """Force the player downward (dive move)."""
    DIVE_FORCE = 15
    if not player.is_grounded:
        player.vel_y = DIVE_FORCE