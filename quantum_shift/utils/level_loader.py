import pygame
import math
from settings import *
from entities.objects import create_object

class LevelLoader:
    """Loads and manages game levels"""
    def __init__(self):
        self.levels = self.create_default_levels()
        self.tile_colors = {
            0: None,  # Empty space
            1: (100, 100, 100),  # Wall
            2: (50, 50, 150),   # Platform
            3: (150, 75, 0),    # Breakable
        }
    
    def create_default_levels(self):
        """Create default levels since we don't have file system access"""
        levels = {}

        # Level 1 - Tutorial
        levels[1] = {
            'name': 'Tutorial',
            'player_start': (50, 400),
            'guards': [(300, 400), (600, 200)],
            'objects': [
                {'type': 'rift', 'x': 700, 'y': 350},
                {'type': 'pressure_plate', 'x': 200, 'y': 450},
                {'type': 'timed_platform', 'x': 400, 'y': 300, 'duration': 3.0}
            ],
            'tiles': self.generate_level_tiles(1),
            'background': 'space_station'
        }

        # Level 2 - Clone Challenge
        levels[2] = {
            'name': 'Clone Protocol',
            'player_start': (50, 300),
            'guards': [(200, 400), (500, 200), (650, 450)],
            'objects': [
                {'type': 'rift', 'x': 720, 'y': 100},
                {'type': 'pressure_plate', 'x': 300, 'y': 450},
                {'type': 'pressure_plate', 'x': 450, 'y': 450},
                {'type': 'moving_platform', 'x': 350, 'y': 250, 
                 'waypoints': [(350, 250), (500, 250)], 'speed': 60},
                {'type': 'portal', 'x': 150, 'y': 200, 'dest_x': 600, 'dest_y': 300}
            ],
            'tiles': self.generate_level_tiles(2),
            'background': 'quantum_lab'
        }

        # Level 3 - Gravity Maze
        levels[3] = {
            'name': 'Gravity Well',
            'player_start': (50, 500),
            'guards': [(300, 300), (500, 150), (650, 400)],
            'objects': [
                {'type': 'rift', 'x': 700, 'y': 50},
                {'type': 'rift', 'x': 100, 'y': 100},
                {'type': 'pressure_plate', 'x': 250, 'y': 150},
                {'type': 'timed_platform', 'x': 400, 'y': 200, 'duration': 2.5},
                {'type': 'moving_platform', 'x': 500, 'y': 350, 
                 'waypoints': [(500, 350), (500, 100)], 'speed': 80}
            ],
            'tiles': self.generate_level_tiles(3),
            'background': 'void_space'
        }

        return levels
    
    def generate_level_tiles(self, level_num):
        """Generate tile layout for level"""
        tiles = []
        rows = SCREEN_HEIGHT // TILE_SIZE
        cols = SCREEN_WIDTH // TILE_SIZE

        for y in range(rows):
            row = []
            for x in range(cols):
                if y == rows - 1 or y == 0 or x == 0 or x == cols - 1:
                    row.append(1)
                elif level_num == 1:
                    if y == rows - 5 and 5 <= x <= 15:
                        row.append(2)
                    elif y == rows - 8 and 20 <= x <= 25:
                        row.append(2)
                    else:
                        row.append(0)
                elif level_num == 2:
                    if (y == rows - 3 and 8 <= x <= 12) or \
                       (y == rows - 6 and 18 <= x <= 22) or \
                       (y == rows - 9 and 5 <= x <= 8):
                        row.append(2)
                    else:
                        row.append(0)
                elif level_num == 3:
                    if (y == 5 and 10 <= x <= 15) or \
                       (y == 10 and 5 <= x <= 8) or \
                       (y == 15 and 20 <= x <= 25):
                        row.append(2)
                    else:
                        row.append(0)
                else:
                    row.append(0)
            tiles.append(row)
        return tiles

    def load_level(self, level_num):
        """Load a specific level"""
        if level_num in self.levels:
            level_data = self.levels[level_num].copy()

            # Don't modify the original objects
            level_data['object_instances'] = []
            for obj_data in level_data['objects']:
                obj_data_copy = obj_data.copy()
                obj_type = obj_data_copy.pop('type')
                obj = create_object(
                    obj_type,
                    obj_data_copy['x'],
                    obj_data_copy['y'],
                    **{k: v for k, v in obj_data_copy.items() if k not in ['x', 'y']}
                )
                level_data['object_instances'].append(obj)
            return level_data
        return None

    def render_level(self, screen, level_data):
        """Render level background and tiles"""
        self.render_background(screen, level_data.get('background', 'default'))

        if 'tiles' in level_data:
            self.render_tiles(screen, level_data['tiles'])

    def render_background(self, screen, background_type):
        """Render animated background"""
        if background_type == 'space_station':
            for i in range(100):
                x = (i * 137) % SCREEN_WIDTH
                y = (i * 211 + pygame.time.get_ticks() // 50) % SCREEN_HEIGHT
                brightness = (i * 17) % 255
                pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)

        elif background_type == 'quantum_lab':
            grid_color = (0, 50, 100)
            for x in range(0, SCREEN_WIDTH, 50):
                pygame.draw.line(screen, grid_color, (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, 50):
                pygame.draw.line(screen, grid_color, (0, y), (SCREEN_WIDTH, y))

        elif background_type == 'void_space':
            center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            time = pygame.time.get_ticks() / 1000.0
            for i in range(20):
                angle = time + i * 0.3
                radius = 50 + i * 15
                x = center_x + math.cos(angle) * radius
                y = center_y + math.sin(angle) * radius
                alpha = max(0, 100 - i * 5)
                if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                    color = (100, 0, 150, alpha)
                    pygame.draw.circle(screen, color[:3], (int(x), int(y)), 3)

    def render_tiles(self, screen, tiles):
        """Render level tiles"""
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile != 0 and tile in self.tile_colors:
                    color = self.tile_colors[tile]
                    if color:
                        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, color, rect)
                        pygame.draw.rect(screen, WHITE, rect, 1)
