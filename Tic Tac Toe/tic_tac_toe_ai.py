# tic_tac_toe_ai.py - Pygame Player vs AI game
import pygame
import random
import time

class TicTacToeAI:
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
        self.YELLOW = (255, 255, 0)
        
        # Game state
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.human_player = 'X'
        self.ai_player = 'O'
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.ai_thinking = False
        self.difficulty = 'hard'  # easy, medium, hard
        self.show_difficulty_menu = True
        
        # Create display
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE + 150))
        pygame.display.set_caption("Tic Tac Toe - Player vs AI")
        
        # Fonts
        self.font_large = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
        
        # AI thinking timer
        self.ai_think_start = 0
        self.ai_think_duration = 1.0  # seconds
    
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
    
    def draw_difficulty_menu(self):
        """Draw the difficulty selection menu"""
        self.screen.fill(self.WHITE)
        
        # Title
        title_text = "Choose AI Difficulty"
        title_surface = self.font_large.render(title_text, True, self.BLACK)
        title_rect = title_surface.get_rect(center=(self.WINDOW_SIZE // 2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Difficulty options
        options = [
            ("1. Easy 😊", "Random moves", self.GREEN),
            ("2. Medium 😐", "Mixed strategy", self.YELLOW),
            ("3. Hard 😈", "Unbeatable AI", self.RED)
        ]
        
        y_start = 200
        for i, (title, desc, color) in enumerate(options):
            # Draw option box
            rect = pygame.Rect(100, y_start + i * 100, 400, 80)
            pygame.draw.rect(self.screen, color, rect, 3)
            
            # Option title
            option_surface = self.font_medium.render(title, True, color)
            option_rect = option_surface.get_rect(center=(rect.centerx, rect.centery - 15))
            self.screen.blit(option_surface, option_rect)
            
            # Option description
            desc_surface = self.font_small.render(desc, True, self.BLACK)
            desc_rect = desc_surface.get_rect(center=(rect.centerx, rect.centery + 15))
            self.screen.blit(desc_surface, desc_rect)
        
        # Instructions
        instruction_text = "Click on a difficulty or press 1, 2, or 3"
        instruction_surface = self.font_small.render(instruction_text, True, self.GRAY)
        instruction_rect = instruction_surface.get_rect(center=(self.WINDOW_SIZE // 2, 550))
        self.screen.blit(instruction_surface, instruction_rect)
    
    def draw_ui(self):
        """Draw the user interface"""
        # Draw bottom panel
        pygame.draw.rect(self.screen, self.LIGHT_BLUE, 
                        (0, self.WINDOW_SIZE, self.WINDOW_SIZE, 150))
        
        # Show difficulty
        diff_text = f"Difficulty: {self.difficulty.upper()}"
        diff_surface = self.font_small.render(diff_text, True, self.BLACK)
        diff_rect = diff_surface.get_rect(topleft=(10, self.WINDOW_SIZE + 10))
        self.screen.blit(diff_surface, diff_rect)
        
        if self.ai_thinking:
            # Show AI thinking animation
            dots = "." * ((pygame.time.get_ticks() // 500) % 4)
            text = f"AI is thinking{dots}"
            text_surface = self.font_medium.render(text, True, self.RED)
            text_rect = text_surface.get_rect(center=(self.WINDOW_SIZE // 2, self.WINDOW_SIZE + 50))
            self.screen.blit(text_surface, text_rect)
        elif not self.game_over:
            if self.current_player == self.human_player:
                text = "Your turn - Click to place X"
                color = self.BLUE
            else:
                text = "AI's turn"
                color = self.RED
            
            text_surface = self.font_medium.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.WINDOW_SIZE // 2, self.WINDOW_SIZE + 50))
            self.screen.blit(text_surface, text_rect)
        else:
            # Show game result
            if self.winner == self.human_player:
                text = "You Win! 🎉"
                color = self.BLUE
            elif self.winner == self.ai_player:
                text = "AI Wins! 🤖"
                color = self.RED
            else:
                text = "It's a Tie! 🤝"
                color = self.GREEN
            
            text_surface = self.font_medium.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.WINDOW_SIZE // 2, self.WINDOW_SIZE + 40))
            self.screen.blit(text_surface, text_rect)
            
            # Show restart instruction
            restart_text = "Click anywhere to play again | Press D for difficulty"
            restart_surface = self.font_small.render(restart_text, True, self.BLACK)
            restart_rect = restart_surface.get_rect(center=(self.WINDOW_SIZE // 2, self.WINDOW_SIZE + 80))
            self.screen.blit(restart_surface, restart_rect)
        
        # Controls
        controls = ["ESC: Exit | R: Restart | D: Change Difficulty"]
        control_surface = self.font_tiny.render(controls[0], True, self.GRAY)
        control_rect = control_surface.get_rect(center=(self.WINDOW_SIZE // 2, self.WINDOW_SIZE + 120))
        self.screen.blit(control_surface, control_rect)
    
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
    
    def make_move(self, row, col, player):
        """Make a move on the board"""
        if self.is_valid_move(row, col):
            self.board[row][col] = player
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
    
    def get_available_moves(self):
        """Get list of available moves"""
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    moves.append((row, col))
        return moves
    
    def minimax(self, board, depth, is_maximizing):
        """Minimax algorithm for AI decision making"""
        # Create temporary board for evaluation
        temp_board = [row[:] for row in self.board]
        self.board = board
        
        winner = self.check_winner()
        
        # Restore board
        self.board = temp_board
        
        # Terminal states
        if winner == self.ai_player:
            return 10 - depth
        elif winner == self.human_player:
            return depth - 10
        elif self.is_board_full_temp(board):
            return 0
        
        if is_maximizing:
            max_eval = float('-inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == '':
                        board[row][col] = self.ai_player
                        eval_score = self.minimax(board, depth + 1, False)
                        board[row][col] = ''
                        max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == '':
                        board[row][col] = self.human_player
                        eval_score = self.minimax(board, depth + 1, True)
                        board[row][col] = ''
                        min_eval = min(min_eval, eval_score)
            return min_eval
    
    def is_board_full_temp(self, board):
        """Check if temporary board is full"""
        for row in board:
            for cell in row:
                if cell == '':
                    return False
        return True
    
    def get_ai_move(self):
        """Get AI move based on difficulty"""
        available_moves = self.get_available_moves()
        
        if not available_moves:
            return None
        
        if self.difficulty == 'easy':
            return random.choice(available_moves)
        elif self.difficulty == 'medium':
            # 70% optimal, 30% random
            if random.random() < 0.7:
                return self.get_best_move()
            else:
                return random.choice(available_moves)
        else:  # hard
            return self.get_best_move()
    
    def get_best_move(self):
        """Get the best move using minimax"""
        best_move = None
        best_value = float('-inf')
        
        temp_board = [row[:] for row in self.board]
        
        for row, col in self.get_available_moves():
            temp_board[row][col] = self.ai_player
            move_value = self.minimax(temp_board, 0, False)
            temp_board[row][col] = ''
            
            if move_value > best_value:
                best_value = move_value
                best_move = (row, col)
        
        return best_move
    
    def start_ai_thinking(self):
        """Start AI thinking animation"""
        self.ai_thinking = True
        self.ai_think_start = time.time()
    
    def handle_difficulty_click(self, pos):
        """Handle clicks in difficulty menu"""
        x, y = pos
        if 100 <= x <= 500:
            if 200 <= y <= 280:
                self.difficulty = 'easy'
                self.show_difficulty_menu = False
            elif 300 <= y <= 380:
                self.difficulty = 'medium'
                self.show_difficulty_menu = False
            elif 400 <= y <= 480:
                self.difficulty = 'hard'
                self.show_difficulty_menu = False
    
    def handle_click(self, pos):
        """Handle mouse click events"""
        if self.show_difficulty_menu:
            self.handle_difficulty_click(pos)
            return
            
        if self.game_over:
            self.reset_game()
            return
        
        if self.current_player != self.human_player or self.ai_thinking:
            return
        
        row, col = self.get_cell_from_mouse(pos)
        if row is not None and col is not None:
            if self.make_move(row, col, self.human_player):
                # Check for winner
                self.winner = self.check_winner()
                if self.winner or self.is_board_full():
                    self.game_over = True
                else:
                    self.current_player = self.ai_player
                    self.start_ai_thinking()
    
    def update_ai(self):
        """Update AI logic"""
        if (self.ai_thinking and 
            time.time() - self.ai_think_start >= self.ai_think_duration):
            
            self.ai_thinking = False
            ai_move = self.get_ai_move()
            
            if ai_move:
                row, col = ai_move
                self.make_move(row, col, self.ai_player)
                
                # Check for winner
                self.winner = self.check_winner()
                if self.winner or self.is_board_full():
                    self.game_over = True
                else:
                    self.current_player = self.human_player
    
    def reset_game(self):
        """Reset the game state"""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = self.human_player
        self.game_over = False
        self.winner = None
        self.ai_thinking = False
    
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
                    elif event.key == pygame.K_r:  # Reset game
                        self.reset_game()
                    elif event.key == pygame.K_d:  # Change difficulty
                        self.show_difficulty_menu = True
                        self.reset_game()
                    elif self.show_difficulty_menu:
                        if event.key == pygame.K_1:
                            self.difficulty = 'easy'
                            self.show_difficulty_menu = False
                        elif event.key == pygame.K_2:
                            self.difficulty = 'medium'
                            self.show_difficulty_menu = False
                        elif event.key == pygame.K_3:
                            self.difficulty = 'hard'
                            self.show_difficulty_menu = False
            
            # Update AI if it's AI's turn
            if not self.show_difficulty_menu and not self.game_over:
                self.update_ai()
            
            # Draw everything
            if self.show_difficulty_menu:
                self.draw_difficulty_menu()
            else:
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
    game = TicTacToeAI()
    game.play()