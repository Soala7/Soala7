# tic_tac_toe_human.py - Pygame Human vs Human game
import pygame
import sys

class TicTacToeHuman:
    def __init__(self):
        pygame.init()
        
        # Game settings
        self.WINDOW_SIZE = 600
        self.GRID_SIZE = 3
        self.CELL_SIZE = self.WINDOW_SIZE // self.GRID_SIZE
        self.LINE_WIDTH = 5
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_BLUE = (173, 216, 230)
        
        # Game state
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        
        # Create display
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE + 100))
        pygame.display.set_caption("Tic Tac Toe - Human vs Human")
        
        # Fonts
        self.font_large = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
    
    def draw_grid(self):
        """Draw the game grid"""
        self.screen.fill(self.WHITE)
        
        # Draw grid lines
        for i in range(1, self.GRID_SIZE):
            # Vertical lines
            pygame.draw.line(self.screen, self.BLACK, 
                           (i * self.CELL_SIZE, 0), 
                           (i * self.CELL_SIZE, self.WINDOW_SIZE), 
                           self.LINE_WIDTH)
            # Horizontal lines
            pygame.draw.line(self.screen, self.BLACK, 
                           (0, i * self.CELL_SIZE), 
                           (self.WINDOW_SIZE, i * self.CELL_SIZE), 
                           self.LINE_WIDTH)
    
    def draw_marks(self):
        """Draw X's and O's on the board"""
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 'X':
                    self.draw_x(row, col)
                elif self.board[row][col] == 'O':
                    self.draw_o(row, col)
    
    def draw_x(self, row, col):
        """Draw an X in the specified cell"""
        center_x = col * self.CELL_SIZE + self.CELL_SIZE // 2
        center_y = row * self.CELL_SIZE + self.CELL_SIZE // 2
        offset = self.CELL_SIZE // 3
        
        # Draw two lines for X
        pygame.draw.line(self.screen, self.BLUE,
                        (center_x - offset, center_y - offset),
                        (center_x + offset, center_y + offset), 8)
        pygame.draw.line(self.screen, self.BLUE,
                        (center_x + offset, center_y - offset),
                        (center_x - offset, center_y + offset), 8)
    
    def draw_o(self, row, col):
        """Draw an O in the specified cell"""
        center_x = col * self.CELL_SIZE + self.CELL_SIZE // 2
        center_y = row * self.CELL_SIZE + self.CELL_SIZE // 2
        radius = self.CELL_SIZE // 3
        
        pygame.draw.circle(self.screen, self.RED, (center_x, center_y), radius, 8)
    
    def draw_ui(self):
        """Draw the user interface"""
        # Draw bottom panel
        pygame.draw.rect(self.screen, self.LIGHT_BLUE, 
                        (0, self.WINDOW_SIZE, self.WINDOW_SIZE, 100))
        
        if not self.game_over:
            # Show current player
            text = f"Current Player: {self.current_player}"
            color = self.BLUE if self.current_player == 'X' else self.RED
            text_surface = self.font_medium.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.WINDOW_SIZE // 2, self.WINDOW_SIZE + 30))
            self.screen.blit(text_surface, text_rect)
        else:
            # Show game result
            if self.winner:
                text = f"Player {self.winner} Wins! 🎉"
                color = self.BLUE if self.winner == 'X' else self.RED
            else:
                text = "It's a Tie! 🤝"
                color = self.GREEN
            
            text_surface = self.font_medium.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.WINDOW_SIZE // 2, self.WINDOW_SIZE + 20))
            self.screen.blit(text_surface, text_rect)
            
            # Show restart instruction
            restart_text = "Click anywhere to play again"
            restart_surface = self.font_small.render(restart_text, True, self.BLACK)
            restart_rect = restart_surface.get_rect(center=(self.WINDOW_SIZE // 2, self.WINDOW_SIZE + 60))
            self.screen.blit(restart_surface, restart_rect)
    
    def get_cell_from_mouse(self, pos):
        """Get board cell from mouse position"""
        x, y = pos
        if y < self.WINDOW_SIZE:  # Only within game area
            col = x // self.CELL_SIZE
            row = y // self.CELL_SIZE
            return row, col
        return None, None
    
    def is_valid_move(self, row, col):
        """Check if the move is valid"""
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ''
    
    def make_move(self, row, col):
        """Make a move on the board"""
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            return True
        return False
    
    def check_winner(self):
        """Check for a winner"""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        
        return None
    
    def is_board_full(self):
        """Check if the board is full"""
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True
    
    def switch_player(self):
        """Switch the current player"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def reset_game(self):
        """Reset the game state"""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def handle_click(self, pos):
        """Handle mouse click events"""
        if self.game_over:
            self.reset_game()
            return
        
        row, col = self.get_cell_from_mouse(pos)
        if row is not None and col is not None:
            if self.make_move(row, col):
                # Check for winner
                self.winner = self.check_winner()
                if self.winner or self.is_board_full():
                    self.game_over = True
                else:
                    self.switch_player()
    
    def draw_winning_line(self):
        """Draw a line through the winning combination"""
        if not self.winner:
            return
        
        # Find winning combination and draw line
        # Check rows
        for i, row in enumerate(self.board):
            if row[0] == row[1] == row[2] == self.winner:
                start_y = i * self.CELL_SIZE + self.CELL_SIZE // 2
                pygame.draw.line(self.screen, self.GREEN,
                               (20, start_y), (self.WINDOW_SIZE - 20, start_y), 10)
                return
        
        # Check columns
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] == self.winner:
                start_x = j * self.CELL_SIZE + self.CELL_SIZE // 2
                pygame.draw.line(self.screen, self.GREEN,
                               (start_x, 20), (start_x, self.WINDOW_SIZE - 20), 10)
                return
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.winner:
            pygame.draw.line(self.screen, self.GREEN,
                           (20, 20), (self.WINDOW_SIZE - 20, self.WINDOW_SIZE - 20), 10)
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] == self.winner:
            pygame.draw.line(self.screen, self.GREEN,
                           (self.WINDOW_SIZE - 20, 20), (20, self.WINDOW_SIZE - 20), 10)
    
    def play(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:  # Reset game with R key
                        self.reset_game()
            
            # Draw everything
            self.draw_grid()
            self.draw_marks()
            if self.game_over and self.winner:
                self.draw_winning_line()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

# Test the game directly if run as main
if __name__ == "__main__":
    game = TicTacToeHuman()
    game.play()