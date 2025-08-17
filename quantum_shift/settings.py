# quantum_shift/settings.py
import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BACKGROUND_COLOR = (10, 10, 30)

# Game settings
GRAVITY = 800
PLAYER_SPEED = 200
JUMP_STRENGTH = 400
TILE_SIZE = 32
TIME_REWIND_DURATION = 5.0  # seconds
CLONE_MAX_COUNT = 3
ENERGY_MAX = 100
ENERGY_REWIND_COST = 20
ENERGY_CLONE_COST = 30
ENERGY_GRAVITY_COST = 15

# Input keys
KEY_UP = pygame.K_w
KEY_DOWN = pygame.K_s
KEY_LEFT = pygame.K_a
KEY_RIGHT = pygame.K_d
KEY_JUMP = pygame.K_SPACE
KEY_REWIND = pygame.K_r
KEY_CLONE = pygame.K_c
KEY_GRAVITY = pygame.K_g
KEY_INTERACT = pygame.K_e

# =============================================================================

