import pygame
import sys
import os
import chess
import time
import threading
import random
from typing import Optional, Tuple
from collections import defaultdict
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
BOARD_SIZE = 700
INFO_PANEL_WIDTH = 250
SQUARE_SIZE = BOARD_SIZE // 8

# Selection screen constants
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 80
FONT_SIZE = 36
BUTTON_SPACING = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
SELECTED_COLOR = (255, 255, 0, 150)
VALID_MOVE_COLOR = (0, 255, 0, 100)
LAST_MOVE_COLOR = (0, 100, 255, 100)
CHECK_COLOR = (255, 0, 0, 150)
PANEL_BG = (45, 45, 45)
TEXT_PRIMARY = (255, 255, 255)
TEXT_SECONDARY = (200, 200, 200)
ACCENT_COLOR = (100, 149, 237)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
BACKGROUND_COLOR = (240, 240, 245)
TITLE_COLOR = (50, 50, 80)

# Calculate centered positions
BOARD_X = (WINDOW_WIDTH - BOARD_SIZE - INFO_PANEL_WIDTH) // 2
BOARD_Y = (WINDOW_HEIGHT - BOARD_SIZE) // 2
INFO_PANEL_X = BOARD_X + BOARD_SIZE

class FastIntermediateChessAI:
    """Fast intermediate chess AI that avoids repetition and responds quickly"""
    
    def __init__(self):
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        
        # Position tables for piece-square evaluation
        self.pawn_table = [
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        
        self.knight_table = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
        ]
        
        # Track move history to avoid repetition
        self.move_history = defaultdict(int)
        self.position_history = set()
        self.last_positions = []
        
        # Transposition table for memoization
        self.transposition_table = {}
        self.max_table_size = 10000
        
    def get_best_move(self, board: chess.Board, max_time: float = 1.0) -> chess.Move:
        """Get best move with time limit and repetition avoidance"""
        start_time = time.time()
        
        # Update position history
        position_key = self._get_position_key(board)
        self.position_history.add(position_key)
        self.last_positions.append(position_key)
        
        # Keep only last 10 positions to prevent memory growth
        if len(self.last_positions) > 10:
            old_pos = self.last_positions.pop(0)
            if self.last_positions.count(old_pos) == 0:
                self.position_history.discard(old_pos)
        
        # Get candidate moves with quick evaluation
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
            
        # Quick move ordering for better alpha-beta pruning
        move_scores = []
        for i, move in enumerate(legal_moves):
            score = self._quick_move_score(board, move)
            # Penalize moves that lead to repetition
            if self._would_repeat_position(board, move):
                score -= 500
            # Add index as tiebreaker to avoid Move comparison
            move_scores.append((score, i, move))
        
        # Sort moves by quick evaluation (best first)
        move_scores.sort(reverse=True, key=lambda x: x[0])
        ordered_moves = [move for _, _, move in move_scores]
        
        # Iterative deepening with time control
        best_move = ordered_moves[0]
        best_score = -float('inf')
        
        for depth in range(1, 6):  # Max depth 5 for speed
            if time.time() - start_time > max_time * 0.8:  # Leave 20% time buffer
                break
                
            try:
                current_best = None
                current_score = -float('inf')
                
                for move in ordered_moves[:15]:  # Limit move evaluation for speed
                    if time.time() - start_time > max_time * 0.9:
                        break
                        
                    board.push(move)
                    score = -self._minimax(board, depth - 1, -float('inf'), float('inf'), False)
                    board.pop()
                    
                    if score > current_score:
                        current_score = score
                        current_best = move
                
                if current_best and current_score > best_score:
                    best_move = current_best
                    best_score = current_score
                    
            except:
                break
        
        # Clean transposition table if it gets too large
        if len(self.transposition_table) > self.max_table_size:
            self.transposition_table.clear()
            
        return best_move
    
    def _minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        """Minimax with alpha-beta pruning and transposition table"""
        
        # Check transposition table
        position_key = self._get_position_key(board)
        if position_key in self.transposition_table:
            cached_depth, cached_score = self.transposition_table[position_key]
            if cached_depth >= depth:
                return cached_score
        
        # Terminal conditions
        if depth == 0 or board.is_game_over():
            score = self._evaluate_board(board)
            self.transposition_table[position_key] = (depth, score)
            return score
        
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return self._evaluate_board(board)
        
        # Quick move ordering for this position
        move_scores = [(self._quick_move_score(board, move), i, move) for i, move in enumerate(legal_moves)]
        move_scores.sort(reverse=maximizing, key=lambda x: x[0])
        ordered_moves = [move for _, _, move in move_scores[:10]]  # Limit for speed
        
        if maximizing:
            max_eval = -float('inf')
            for move in ordered_moves:
                board.push(move)
                eval_score = self._minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            
            self.transposition_table[position_key] = (depth, max_eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in ordered_moves:
                board.push(move)
                eval_score = self._minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            
            self.transposition_table[position_key] = (depth, min_eval)
            return min_eval
    
    def _quick_move_score(self, board: chess.Board, move: chess.Move) -> float:
        """Quick move evaluation for ordering"""
        score = 0
        
        # Capture value
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                score += self.piece_values[captured_piece.piece_type]
            
            # Moving piece value (prefer lower value pieces capturing higher)
            moving_piece = board.piece_at(move.from_square)
            if moving_piece:
                score -= self.piece_values[moving_piece.piece_type] // 10
        
        # Check bonus
        board.push(move)
        if board.is_check():
            score += 50
        board.pop()
        
        # Central control
        center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        if move.to_square in center_squares:
            score += 20
        
        return score
    
    def _would_repeat_position(self, board: chess.Board, move: chess.Move) -> bool:
        """Check if move would create a position we've seen before"""
        board.push(move)
        position_key = self._get_position_key(board)
        would_repeat = position_key in self.position_history
        board.pop()
        return would_repeat
    
    def _get_position_key(self, board: chess.Board) -> str:
        """Generate a unique key for the current position"""
        return board.fen().split(' ')[0]  # Just piece positions, ignore move counts
    
    def _evaluate_board(self, board: chess.Board) -> float:
        """Enhanced board evaluation function"""
        if board.is_checkmate():
            return -30000 if board.turn else 30000
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        score = 0
        
        # Material and positional evaluation
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Material value
                piece_value = self.piece_values[piece.piece_type]
                
                # Positional bonus
                positional_bonus = 0
                if piece.piece_type == chess.PAWN:
                    idx = square if piece.color == chess.WHITE else chess.square_mirror(square)
                    positional_bonus = self.pawn_table[idx]
                elif piece.piece_type == chess.KNIGHT:
                    idx = square if piece.color == chess.WHITE else chess.square_mirror(square)
                    positional_bonus = self.knight_table[idx]
                
                total_value = piece_value + positional_bonus
                score += total_value if piece.color == chess.WHITE else -total_value
        
        # Mobility bonus (number of legal moves)
        current_mobility = len(list(board.legal_moves))
        
        # Safely check opponent mobility
        try:
            board.push(chess.Move.null())  # Pass turn
            if not board.is_game_over():
                opponent_mobility = len(list(board.legal_moves))
            else:
                opponent_mobility = 0
            board.pop()
        except:
            # If null move not supported, skip mobility evaluation
            opponent_mobility = current_mobility
        
        mobility_bonus = (current_mobility - opponent_mobility) * 2
        score += mobility_bonus if board.turn == chess.WHITE else -mobility_bonus
        
        # King safety
        white_king = board.king(chess.WHITE)
        black_king = board.king(chess.BLACK)
        
        if white_king and black_king:
            # Penalize exposed kings
            white_king_attacks = len(board.attackers(chess.BLACK, white_king))
            black_king_attacks = len(board.attackers(chess.WHITE, black_king))
            score -= (white_king_attacks - black_king_attacks) * 20
        
        return score

class ChessGame:
    """Base chess game class"""
    
    def __init__(self, ai_mode=False, difficulty=2):
        self.board = chess.Board()
        self.ai_mode = ai_mode
        self.ai = FastIntermediateChessAI() if ai_mode else None
        self.ai_color = chess.BLACK if ai_mode else None
        self.human_color = chess.WHITE if ai_mode else None
        self.last_move = None
        self.game_over = False
        self.move_times = []
        self.difficulty = difficulty
        self.ai_thinking = False
        self.current_player = chess.WHITE  # For human vs human
    
    def set_difficulty(self, difficulty: int):
        """Change AI difficulty level (1-3)"""
        self.difficulty = difficulty
        print(f"AI difficulty set to {['Easy', 'Medium', 'Hard'][difficulty-1]}")
    
    def make_move(self, move: chess.Move) -> bool:
        """Make a move (works for both AI and human modes)"""
        if self.game_over:
            return False
        
        if self.ai_mode:
            # AI mode - only allow human moves on human's turn
            if self.board.turn != self.human_color or self.ai_thinking:
                return False
        
        if move in self.board.legal_moves:
            self.board.push(move)
            self.last_move = move
            self._check_game_over()
            if not self.ai_mode:
                self.current_player = not self.current_player
            return True
        return False
    
    def make_ai_move(self, max_time: float = 1.5) -> Optional[chess.Move]:
        """Have the AI make its move with time limit"""
        if not self.ai_mode or self.game_over or self.board.turn != self.ai_color:
            return None
        
        self.ai_thinking = True
        start_time = time.time()
        
        # Adjust thinking time based on difficulty
        thinking_times = {1: 0.1, 2: 0.5, 3: max_time}
        actual_time = thinking_times.get(self.difficulty, max_time)
        
        if self.difficulty == 1:
            # Easy - random moves
            legal_moves = list(self.board.legal_moves)
            move = random.choice(legal_moves) if legal_moves else None
        else:
            # Medium/Hard - use AI
            move = self.ai.get_best_move(self.board, actual_time)
        
        move_time = time.time() - start_time
        
        if move:
            self.board.push(move)
            self.last_move = move
            self.move_times.append(move_time)
            self._check_game_over()
            
        self.ai_thinking = False
        return move
    
    def _check_game_over(self):
        """Check if the game is over"""
        self.game_over = self.board.is_game_over()
    
    def get_game_state(self) -> str:
        """Get current game state description"""
        if self.ai_thinking:
            return "AI thinking..."
        elif self.board.is_checkmate():
            if self.ai_mode:
                return "Checkmate! You win!" if self.board.turn == self.ai_color else "Checkmate! AI wins!"
            else:
                winner = "Black" if self.board.turn == chess.WHITE else "White"
                return f"Checkmate! {winner} wins!"
        elif self.board.is_stalemate():
            return "Stalemate!"
        elif self.board.is_insufficient_material():
            return "Draw - insufficient material"
        elif self.board.is_seventyfive_moves():
            return "Draw - 75 move rule"
        elif self.board.is_fivefold_repetition():
            return "Draw - fivefold repetition"
        elif self.board.is_check():
            return "Check!"
        else:
            return "Game in progress"
    
    def get_average_move_time(self) -> float:
        """Get average AI move time"""
        return sum(self.move_times) / len(self.move_times) if self.move_times else 0
    
    def reset(self):
        """Reset the game state"""
        self.board.reset()
        if self.ai_mode:
            self.ai = FastIntermediateChessAI()  # Reset AI state
        self.last_move = None
        self.game_over = False
        self.move_times = []
        self.ai_thinking = False
        self.current_player = chess.WHITE

class PieceRenderer:
    """Handles loading and drawing chess pieces"""
    
    def __init__(self):
        self.piece_images = {}
        self.load_piece_images()
    
    def load_piece_images(self):
        """Load piece images from assets or create Unicode fallbacks"""
        piece_symbols = {
            'P': chess.PAWN, 'R': chess.ROOK, 'N': chess.KNIGHT,
            'B': chess.BISHOP, 'Q': chess.QUEEN, 'K': chess.KING
        }
        
        for symbol, piece_type in piece_symbols.items():
            for color in [chess.WHITE, chess.BLACK]:
                try:
                    # Try to load image files
                    color_name = 'white' if color == chess.WHITE else 'black'
                    piece_name = chess.piece_name(piece_type).lower()
                    img_path = os.path.join("assets", "pieces", f"{color_name}_{piece_name}.png")
                    if os.path.exists(img_path):
                        image = pygame.image.load(img_path)
                        self.piece_images[(piece_type, color)] = pygame.transform.scale(
                            image, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
                    else:
                        raise FileNotFoundError
                except:
                    # Fallback to Unicode symbols
                    self._create_unicode_piece(piece_type, color)
    
    def _create_unicode_piece(self, piece_type: int, color: bool):
        """Create piece using Unicode symbols if images not available"""
        symbols = {
            (chess.KING, chess.WHITE): '♔', (chess.QUEEN, chess.WHITE): '♕',
            (chess.ROOK, chess.WHITE): '♖', (chess.BISHOP, chess.WHITE): '♗',
            (chess.KNIGHT, chess.WHITE): '♘', (chess.PAWN, chess.WHITE): '♙',
            (chess.KING, chess.BLACK): '♚', (chess.QUEEN, chess.BLACK): '♛',
            (chess.ROOK, chess.BLACK): '♜', (chess.BISHOP, chess.BLACK): '♝',
            (chess.KNIGHT, chess.BLACK): '♞', (chess.PAWN, chess.BLACK): '♟'
        }
        
        font = pygame.font.Font(None, SQUARE_SIZE - 10)
        symbol = symbols[(piece_type, color)]
        text_color = (240, 240, 240) if color == chess.WHITE else (40, 40, 40)
        text = font.render(symbol, True, text_color)
        
        surface = pygame.Surface((SQUARE_SIZE - 20, SQUARE_SIZE - 20), pygame.SRCALPHA)
        text_rect = text.get_rect(center=(surface.get_width()//2, surface.get_height()//2))
        surface.blit(text, text_rect)
        
        self.piece_images[(piece_type, color)] = surface
    
    def draw_piece(self, surface: pygame.Surface, piece: chess.Piece, x: int, y: int):
        """Draw a piece at the specified position"""
        image = self.piece_images.get((piece.piece_type, piece.color))
        if image:
            surface.blit(image, (x + 10, y + 10))

class Button:
    """Enhanced button class with better visuals"""
    
    def __init__(self, x, y, width, height, text, 
                 color=LIGHT_BLUE, hover_color=DARK_BLUE, 
                 text_color=BLACK, shadow=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.shadow = shadow
        self.click_offset = 2 if shadow else 0
        
    def draw(self, surface, font):
        """Draw the button with nice effects"""
        # Draw shadow if enabled
        if self.shadow and not self.is_hovered:
            shadow_rect = self.rect.move(5, 5)
            pygame.draw.rect(surface, (200, 200, 200), shadow_rect, border_radius=12)
        
        # Draw main button
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        
        # Draw border
        border_color = (100, 100, 100) if not self.is_hovered else (50, 50, 50)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=10)
        
        # Draw text with slight offset when clicked
        text_pos = self.rect.center
        if self.is_hovered and pygame.mouse.get_pressed()[0]:
            text_pos = (text_pos[0], text_pos[1] + self.click_offset)
        
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=text_pos)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        """Check if mouse is hovering over the button"""
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        """Check if button was clicked"""
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class GameUI:
    """Handles all game rendering and input"""
    
    def __init__(self, game: ChessGame):
        self.game = game
        self.piece_renderer = PieceRenderer()
        self.selected_square = None
        self.board_flipped = False
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Set up window
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess Game")
    
    def draw_board(self):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(
                    BOARD_X + col * SQUARE_SIZE,
                    BOARD_Y + row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)
    
    def draw_pieces(self):
        """Draw all pieces on the board"""
        for square in chess.SQUARES:
            piece = self.game.board.piece_at(square)
            if piece:
                row, col = self._square_to_pos(square)
                x = BOARD_X + col * SQUARE_SIZE
                y = BOARD_Y + row * SQUARE_SIZE
                self.piece_renderer.draw_piece(self.screen, piece, x, y)
    
    def draw_highlights(self):
        """Highlight selected square, valid moves, etc."""
        # Highlight last move
        if self.game.last_move:
            for square in [self.game.last_move.from_square, self.game.last_move.to_square]:
                row, col = self._square_to_pos(square)
                rect = pygame.Rect(
                    BOARD_X + col * SQUARE_SIZE,
                    BOARD_Y + row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill(LAST_MOVE_COLOR)
                self.screen.blit(highlight, rect)
        
        # Highlight selected square
        if self.selected_square:
            row, col = self._square_to_pos(self.selected_square)
            rect = pygame.Rect(
                BOARD_X + col * SQUARE_SIZE,
                BOARD_Y + row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            )
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill(SELECTED_COLOR)
            self.screen.blit(highlight, rect)
            
            # Highlight valid moves
            for move in self.game.board.legal_moves:
                if move.from_square == self.selected_square:
                    row, col = self._square_to_pos(move.to_square)
                    center_x = BOARD_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = BOARD_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
                    
                    if self.game.board.piece_at(move.to_square):  # Capture
                        pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), SQUARE_SIZE//3, 4)
                    else:  # Normal move
                        pygame.draw.circle(self.screen, (0, 255, 0), (center_x, center_y), 10)
        
        # Highlight check
        if self.game.board.is_check():
            king_square = self.game.board.king(self.game.board.turn)
            if king_square:
                row, col = self._square_to_pos(king_square)
                rect = pygame.Rect(
                    BOARD_X + col * SQUARE_SIZE,
                    BOARD_Y + row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill(CHECK_COLOR)
                self.screen.blit(highlight, rect)
    
    def draw_info_panel(self):
        """Draw the right-side information panel"""
        panel = pygame.Rect(INFO_PANEL_X, 0, INFO_PANEL_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, PANEL_BG, panel)
        
        y_offset = 20
        
        # Game title
        title = "Chess vs AI" if self.game.ai_mode else "Chess vs Human"
        title_surface = self.font_large.render(title, True, TEXT_PRIMARY)
        self.screen.blit(title_surface, (INFO_PANEL_X + 20, y_offset))
        y_offset += 50
        
        # Current turn
        if self.game.ai_mode:
            if self.game.ai_thinking:
                turn_text = "AI thinking..."
            else:
                turn_text = "Your turn" if self.game.board.turn == chess.WHITE else "AI's turn"
        else:
            current_color = "White" if self.game.board.turn == chess.WHITE else "Black"
            turn_text = f"{current_color}'s turn"
            
        turn_surface = self.font_medium.render(turn_text, True, TEXT_PRIMARY)
        self.screen.blit(turn_surface, (INFO_PANEL_X + 20, y_offset))
        y_offset += 40
        
        # Game status
        status = self.game.get_game_state()
        status_color = TEXT_PRIMARY
        if "wins" in status.lower():
            if self.game.ai_mode:
                status_color = (255, 100, 100) if "AI wins" in status else (100, 255, 100)
            else:
                status_color = (100, 255, 100)
        elif "Check" in status:
            status_color = (255, 150, 150)
        
        status_surface = self.font_medium.render(status, True, status_color)
        self.screen.blit(status_surface, (INFO_PANEL_X + 20, y_offset))
        y_offset += 50
        
        if self.game.ai_mode:
            # Difficulty level
            diff_names = {1: "Easy", 2: "Medium", 3: "Hard"}
            diff_text = f"AI Level: {diff_names.get(self.game.difficulty, 'Medium')}"
            diff_surface = self.font_small.render(diff_text, True, TEXT_SECONDARY)
            self.screen.blit(diff_surface, (INFO_PANEL_X + 20, y_offset))
            y_offset += 30
            
            # Average AI move time
            if self.game.move_times:
                avg_time = f"AI time: {self.game.get_average_move_time():.2f}s"
                time_surface = self.font_small.render(avg_time, True, TEXT_SECONDARY)
                self.screen.blit(time_surface, (INFO_PANEL_X + 20, y_offset))
                y_offset += 40
        
        # Move count
        move_count = f"Moves: {len(self.game.board.move_stack)}"
        move_surface = self.font_small.render(move_count, True, TEXT_SECONDARY)
        self.screen.blit(move_surface, (INFO_PANEL_X + 20, y_offset))
        y_offset += 40
        
        # Controls help
        controls = []
        if self.game.ai_mode:
            controls = [
                "Controls:",
                "Click - Select/move",
                "1/2/3 - AI difficulty",
                "R - Reset game",
                "F - Flip board",
                "M - Main menu",
                "ESC - Quit"
            ]
        else:
            controls = [
                "Controls:",
                "Click - Select/move",
                "R - Reset game", 
                "F - Flip board",
                "M - Main menu",
                "ESC - Quit"
            ]
        
        for control in controls:
            control_surface = self.font_small.render(control, True, TEXT_SECONDARY)
            self.screen.blit(control_surface, (INFO_PANEL_X + 20, y_offset))
            y_offset += 25
    
    def _square_to_pos(self, square: chess.Square) -> Tuple[int, int]:
        """Convert chess square to board coordinates"""
        if self.board_flipped:
            return (7 - chess.square_rank(square)), (7 - chess.square_file(square))
        return (7 - chess.square_rank(square)), chess.square_file(square)
    
    def _pos_to_square(self, row: int, col: int) -> chess.Square:
        """Convert board coordinates to chess square"""
        if self.board_flipped:
            return chess.square(7 - col, 7 - row)
        return chess.square(col, 7 - row)
    
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Handle mouse click on the board"""
        if self.game.game_over:
            return False
            
        if self.game.ai_mode and (self.game.board.turn != chess.WHITE or self.game.ai_thinking):
            return False
        
        # Check if click is on board
        if (BOARD_X <= pos[0] < BOARD_X + BOARD_SIZE and
            BOARD_Y <= pos[1] < BOARD_Y + BOARD_SIZE):
            
            col = (pos[0] - BOARD_X) // SQUARE_SIZE
            row = (pos[1] - BOARD_Y) // SQUARE_SIZE
            square = self._pos_to_square(row, col)
            piece = self.game.board.piece_at(square)
            
            if self.selected_square is None:
                # Select a piece
                if piece:
                    if self.game.ai_mode:
                        # In AI mode, only allow selecting white pieces
                        if piece.color == chess.WHITE:
                            self.selected_square = square
                            return True
                    else:
                        # In human vs human, allow selecting current player's pieces
                        if piece.color == self.game.board.turn:
                            self.selected_square = square
                            return True
            else:
                # Try to make a move
                move = self._create_move(self.selected_square, square)
                if move and move in self.game.board.legal_moves:
                    if self.game.make_move(move):
                        self.selected_square = None
                        return True
                
                # Select different piece
                if piece:
                    if self.game.ai_mode:
                        if piece.color == chess.WHITE:
                            self.selected_square = square
                            return True
                    else:
                        if piece.color == self.game.board.turn:
                            self.selected_square = square
                            return True
                
                self.selected_square = None
                return False
        
        return False
    
    def _create_move(self, from_square: chess.Square, to_square: chess.Square) -> Optional[chess.Move]:
        """Create a move object, handling promotions"""
        promotion = None
        piece = self.game.board.piece_at(from_square)
        
        if piece and piece.piece_type == chess.PAWN:
            to_rank = chess.square_rank(to_square)
            if (piece.color == chess.WHITE and to_rank == 7) or \
               (piece.color == chess.BLACK and to_rank == 0):
                promotion = chess.QUEEN  # Auto-queen for simplicity
        
        return chess.Move(from_square, to_square, promotion)
    
    def draw(self):
        """Draw the complete game interface"""
        self.screen.fill(WHITE)
        self.draw_board()
        self.draw_highlights()
        self.draw_pieces()
        self.draw_info_panel()

def draw_chess_icon(surface, x, y, size):
    """Draw a simple chess piece icon"""
    # Draw chess board background
    square_size = size // 8
    for row in range(8):
        for col in range(8):
            color = LIGHT_BLUE if (row + col) % 2 == 0 else DARK_BLUE
            rect = pygame.Rect(x + col*square_size, y + row*square_size, square_size, square_size)
            pygame.draw.rect(surface, color, rect)
    
    # Draw simple king and queen pieces
    king_font = pygame.font.Font(None, size//2)
    queen_font = pygame.font.Font(None, size//2)
    
    king = king_font.render("♔", True, WHITE)
    queen = queen_font.render("♕", True, BLACK)
    
    surface.blit(king, (x + size//4 - king.get_width()//2, y + size//4 - king.get_height()//2))
    surface.blit(queen, (x + 3*size//4 - queen.get_width()//2, y + 3*size//4 - queen.get_height()//2))

def run_selection_screen():
    """Run the opponent selection screen with improved visuals"""
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chess Game - Select Opponent")
    
    # Fonts
    try:
        font_large = pygame.font.Font(None, 60)
        font_medium = pygame.font.Font(None, FONT_SIZE)
    except:
        font_large = pygame.font.Font(None, 60)
        font_medium = pygame.font.Font(None, FONT_SIZE)
    
    # Calculate centered positions
    button_area_height = 2*BUTTON_HEIGHT + BUTTON_SPACING
    start_y = (600 - button_area_height) // 2
    
    # Create buttons with better styling
    human_button = Button(
        800//2 - BUTTON_WIDTH//2, 
        start_y, 
        BUTTON_WIDTH, 
        BUTTON_HEIGHT, 
        "Human vs Human",
        color=(220, 235, 245),
        hover_color=(150, 200, 235),
        text_color=(40, 60, 80)
    )
    
    ai_button = Button(
        800//2 - BUTTON_WIDTH//2, 
        start_y + BUTTON_HEIGHT + BUTTON_SPACING, 
        BUTTON_WIDTH, 
        BUTTON_HEIGHT, 
        "Human vs AI",
        color=(245, 220, 220),
        hover_color=(235, 150, 150),
        text_color=(80, 40, 40)
    )
    
    # Create title with shadow effect
    title_text = font_large.render("Select Game Mode", True, TITLE_COLOR)
    title_shadow = font_large.render("Select Game Mode", True, (180, 180, 200))
    title_rect = title_text.get_rect(center=(800//2, 120))
    
    # Chess icon
    icon_size = 120
    icon_x = 800//2 - icon_size//2
    icon_y = title_rect.bottom + 30
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            # Check button clicks
            if human_button.is_clicked(mouse_pos, event):
                print("Launching human vs human game...")
                run_chess_game(ai_mode=False)
                return
                
            if ai_button.is_clicked(mouse_pos, event):
                print("Launching human vs AI game...")
                run_chess_game(ai_mode=True)
                return
        
        # Check button hovers
        human_button.check_hover(mouse_pos)
        ai_button.check_hover(mouse_pos)
        
        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        
        # Draw decorative chess board pattern in background
        for i in range(0, 800, 40):
            for j in range(0, 600, 40):
                if (i//40 + j//40) % 2 == 0:
                    pygame.draw.rect(screen, (230, 230, 235), (i, j, 40, 40))
        
        # Draw title with shadow
        screen.blit(title_shadow, title_rect.move(3, 3))
        screen.blit(title_text, title_rect)
        
        # Draw chess icon
        draw_chess_icon(screen, icon_x, icon_y, icon_size)
        
        # Draw buttons
        human_button.draw(screen, font_medium)
        ai_button.draw(screen, font_medium)
        
        # Draw version info
        version_text = font_medium.render("Chess Game v1.0", True, (150, 150, 150))
        screen.blit(version_text, (20, 600 - 40))
        
        pygame.display.flip()

def run_chess_game(ai_mode=False):
    """Run the main chess game"""
    try:
        game = ChessGame(ai_mode=ai_mode, difficulty=2)
        ui = GameUI(game)
        clock = pygame.time.Clock()
        
        mode_text = "Chess vs AI" if ai_mode else "Chess vs Human"
        print(f"{mode_text} started!")
        print("Controls:")
        if ai_mode:
            print("1/2/3: Change AI difficulty (Easy/Medium/Hard)")
        print("R: Reset game")
        print("F: Flip board")
        print("M: Return to main menu")
        print("ESC: Quit")
        print("Click pieces and squares to move")
        
        # AI move thread for non-blocking AI thinking
        ai_move_thread = None
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        ui.handle_click(event.pos)
                elif event.type == KEYDOWN:
                    if ai_mode and event.key == K_1:
                        game.set_difficulty(1)
                    elif ai_mode and event.key == K_2:
                        game.set_difficulty(2)
                    elif ai_mode and event.key == K_3:
                        game.set_difficulty(3)
                    elif event.key == K_r:
                        # Wait for AI thread to finish before resetting
                        if ai_move_thread and ai_move_thread.is_alive():
                            ai_move_thread.join()
                        game.reset()
                        ui.selected_square = None
                        print("Game reset")
                    elif event.key == K_f:
                        ui.board_flipped = not ui.board_flipped
                        ui.selected_square = None  # Clear selection when flipping
                        print("Board flipped" if ui.board_flipped else "Board normal")
                    elif event.key == K_m:
                        # Return to main menu
                        if ai_move_thread and ai_move_thread.is_alive():
                            ai_move_thread.join()
                        run_selection_screen()
                        return
                    elif event.key == K_ESCAPE:
                        running = False
            
            # AI move handling with threading for non-blocking UI
            if (ai_mode and not game.game_over and 
                game.board.turn == chess.BLACK and 
                not game.ai_thinking and 
                (ai_move_thread is None or not ai_move_thread.is_alive())):
                
                def ai_move_worker():
                    move = game.make_ai_move(max_time=1.5)
                    if move:
                        print(f"AI played: {move}")
                
                ai_move_thread = threading.Thread(target=ai_move_worker)
                ai_move_thread.daemon = True
                ai_move_thread.start()
            
            ui.draw()
            pygame.display.flip()
            clock.tick(60)
        
        # Wait for AI thread to finish before quitting
        if ai_move_thread and ai_move_thread.is_alive():
            ai_move_thread.join()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function - starts with selection screen"""
    print("Welcome to Chess Game!")
    run_selection_screen()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()