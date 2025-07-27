import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + GRID_X_OFFSET * 2 + 200
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + GRID_Y_OFFSET * 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Tetris pieces (tetrominoes)
PIECES = {
    'I': [['.....',
           '..#..',
           '..#..',
           '..#..',
           '..#..'],
          ['.....',
           '.....',
           '####.',
           '.....',
           '.....']],
    
    'O': [['.....',
           '.....',
           '.##..',
           '.##..',
           '.....']],
    
    'T': [['.....',
           '.....',
           '.#...',
           '###..',
           '.....'],
          ['.....',
           '.....',
           '.#...',
           '.##..',
           '.#...'],
          ['.....',
           '.....',
           '.....',
           '###..',
           '.#...'],
          ['.....',
           '.....',
           '.#...',
           '##...',
           '.#...']],
    
    'S': [['.....',
           '.....',
           '.##..',
           '##...',
           '.....'],
          ['.....',
           '.#...',
           '.##..',
           '..#..',
           '.....']],
    
    'Z': [['.....',
           '.....',
           '##...',
           '.##..',
           '.....'],
          ['.....',
           '..#..',
           '.##..',
           '.#...',
           '.....']],
    
    'J': [['.....',
           '.#...',
           '.#...',
           '##...',
           '.....'],
          ['.....',
           '.....',
           '#....',
           '###..',
           '.....'],
          ['.....',
           '.##..',
           '.#...',
           '.#...',
           '.....'],
          ['.....',
           '.....',
           '###..',
           '..#..',
           '.....']],
    
    'L': [['.....',
           '..#..',
           '..#..',
           '.##..',
           '.....'],
          ['.....',
           '.....',
           '###..',
           '#....',
           '.....'],
          ['.....',
           '##...',
           '.#...',
           '.#...',
           '.....'],
          ['.....',
           '.....',
           '..#..',
           '###..',
           '.....']]
}

PIECE_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        
    def get_new_piece(self):
        piece_type = random.choice(list(PIECES.keys()))
        return {
            'type': piece_type,
            'x': GRID_WIDTH // 2 - 2,
            'y': 0,
            'rotation': 0,
            'shape': PIECES[piece_type][0]
        }
    
    def rotate_piece(self, piece):
        piece_type = piece['type']
        rotations = PIECES[piece_type]
        new_rotation = (piece['rotation'] + 1) % len(rotations)
        return new_rotation, rotations[new_rotation]
    
    def is_valid_position(self, piece, dx=0, dy=0, rotation=None):
        if rotation is None:
            shape = piece['shape']
        else:
            shape = PIECES[piece['type']][rotation]
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '#':
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or
                        (new_y >= 0 and self.grid[new_y][new_x] != 0)):
                        return False
        return True
    
    def place_piece(self, piece):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell == '#':
                    grid_x = piece['x'] + x
                    grid_y = piece['y'] + y
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = piece['type']
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(cell != 0 for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        lines_cleared = len(lines_to_clear)
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            self.score += lines_cleared * 100 * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(50, 500 - (self.level - 1) * 50)
        
        return lines_cleared
    
    def is_game_over(self):
        return not self.is_valid_position(self.current_piece)
    
    def move_piece(self, dx, dy):
        if self.is_valid_position(self.current_piece, dx, dy):
            self.current_piece['x'] += dx
            self.current_piece['y'] += dy
            return True
        return False
    
    def rotate_current_piece(self):
        new_rotation, new_shape = self.rotate_piece(self.current_piece)
        if self.is_valid_position(self.current_piece, rotation=new_rotation):
            self.current_piece['rotation'] = new_rotation
            self.current_piece['shape'] = new_shape
    
    def drop_piece(self):
        if not self.move_piece(0, 1):
            self.place_piece(self.current_piece)
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.get_new_piece()
            return True
        return False
    
    def hard_drop(self):
        while self.move_piece(0, 1):
            self.score += 1
        self.drop_piece()

def draw_grid(screen, tetris):
    # Draw the game grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(
                GRID_X_OFFSET + x * CELL_SIZE,
                GRID_Y_OFFSET + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            
            if tetris.grid[y][x] != 0:
                color = PIECE_COLORS[tetris.grid[y][x]]
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)
            else:
                pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)

def draw_piece(screen, piece):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell == '#':
                rect = pygame.Rect(
                    GRID_X_OFFSET + (piece['x'] + x) * CELL_SIZE,
                    GRID_Y_OFFSET + (piece['y'] + y) * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                color = PIECE_COLORS[piece['type']]
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

def draw_next_piece(screen, piece, font):
    text = font.render("Next:", True, WHITE)
    screen.blit(text, (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20, GRID_Y_OFFSET))
    
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell == '#':
                rect = pygame.Rect(
                    GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20 + x * 20,
                    GRID_Y_OFFSET + 30 + y * 20,
                    20,
                    20
                )
                color = PIECE_COLORS[piece['type']]
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

def draw_info(screen, tetris, font):
    info_x = GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20
    
    score_text = font.render(f"Score: {tetris.score}", True, WHITE)
    screen.blit(score_text, (info_x, GRID_Y_OFFSET + 120))
    
    level_text = font.render(f"Level: {tetris.level}", True, WHITE)
    screen.blit(level_text, (info_x, GRID_Y_OFFSET + 150))
    
    lines_text = font.render(f"Lines: {tetris.lines_cleared}", True, WHITE)
    screen.blit(lines_text, (info_x, GRID_Y_OFFSET + 180))
    
    # Controls
    controls = [
        "Controls:",
        "A/D - Move",
        "S - Soft drop",
        "W - Rotate",
        "Space - Hard drop",
        "R - Restart"
    ]
    
    for i, control in enumerate(controls):
        text = font.render(control, True, WHITE)
        screen.blit(text, (info_x, GRID_Y_OFFSET + 220 + i * 20))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
    tetris = Tetris()
    running = True
    game_over = False
    
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        tetris = Tetris()
                        game_over = False
                else:
                    if event.key == pygame.K_a:
                        tetris.move_piece(-1, 0)
                    elif event.key == pygame.K_d:
                        tetris.move_piece(1, 0)
                    elif event.key == pygame.K_s:
                        tetris.drop_piece()
                    elif event.key == pygame.K_w:
                        tetris.rotate_current_piece()
                    elif event.key == pygame.K_SPACE:
                        tetris.hard_drop()
                    elif event.key == pygame.K_r:
                        tetris = Tetris()
        
        if not game_over:
            # Handle automatic piece falling
            tetris.fall_time += dt
            if tetris.fall_time >= tetris.fall_speed:
                tetris.drop_piece()
                tetris.fall_time = 0
            
            # Check for game over
            if tetris.is_game_over():
                game_over = True
        
        # Draw everything
        screen.fill(BLACK)
        draw_grid(screen, tetris)
        
        if not game_over:
            draw_piece(screen, tetris.current_piece)
        
        draw_next_piece(screen, tetris.next_piece, font)
        draw_info(screen, tetris, font)
        
        if game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            restart_text = font.render("Press R to restart", True, WHITE)
            screen.blit(game_over_text, (GRID_X_OFFSET + 50, GRID_Y_OFFSET + 200))
            screen.blit(restart_text, (GRID_X_OFFSET + 30, GRID_Y_OFFSET + 230))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()