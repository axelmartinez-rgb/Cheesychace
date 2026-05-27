# movement.py
# Handles player movement and crash detection

JUMP_FORCE   = -15   # Must match characters.py
SCROLL_SPEED = 5     # Must match main.py


def handle_jump(player, events):
    """Check for jump input and apply jump force."""
    import pygame
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if player.is_grounded:
                player.vel_y       = JUMP_FORCE
                player.is_grounded = False


def check_crash(player, obstacles):
    """
    Check if player collided with a non-platform obstacle.
    Returns the name of the object hit, or None if no crash.
    """
    for obj in obstacles:
        if player.rect.colliderect(obj.rect):
            if not obj.is_platform:
                return obj.name
    return None