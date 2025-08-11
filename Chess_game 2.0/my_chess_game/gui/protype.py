import pygame
import sys
import os
import numpy as np
import chess
from typing import List, Tuple, Optional, Dict

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
BOARD_WIDTH = 600
BOARD_HEIGHT = 600
INFO_PANEL_WIDTH = 200
WINDOW_WIDTH = BOARD_WIDTH + INFO_PANEL_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT

ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
SELECTED_COLOR = (255, 255, 0, 150)
VALID_MOVE_COLOR = (0, 255, 0, 100)
LAST_MOVE_COLOR = (0, 100, 255, 100)
CHECK_COLOR = (255, 0, 0, 150)
CAPTURE_COLOR = (255, 100, 100, 150)

# Info panel colors
PANEL_BG = (45, 45, 45)
TEXT_PRIMARY = (255, 255, 255)
TEXT_SECONDARY = (200, 200, 200)
ACCENT_COLOR = (100, 149, 237)

# Set up window
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Advanced Chess Game with python-chess")

class SoundEngine:
    def __init__(self):
        self.sounds = {}
        self.enabled = True
        self.volume = 0.5
        self.initialize_sounds()
    
    def initialize_sounds(self):
        sound_files = {
            'move': 'move-self.mp3',
            'checkmate': 'game-end.webm',
            'promotion': 'promote.mp3',
            'check': 'move-check.mp3',
            'castle': 'castle.mp3',
            'capture': 'capture.mp3'
        }
        
        for name, filename in sound_files.items():
            try:
                path = os.path.join("Chess_game 2.0/assets", filename)
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                    print(f"Loaded sound: {filename}")
                else:
                    print(f"Warning: Sound file {path} not found")
                    self.sounds[name] = None
            except Exception as e:
                print(f"Warning: Could not load sound {filename}: {e}")
                self.sounds[name] = None
    
    def play(self, sound_name: str):
        if not self.enabled or sound_name not in self.sounds:
            return
        sound = self.sounds[sound_name]
        if sound:
            try:
                sound.set_volume(self.volume)
                sound.play()
            except Exception as e:
                print(f'Error playing sound {sound_name}: {e}')

class PieceRenderer:
    """Handles piece image loading and rendering"""
    
    def __init__(self):
        self.piece_images = {}
        self.load_piece_images()
    
    def load_piece_images(self):
        """Load or create piece images"""
        piece_symbols = {
            'P': chess.PAWN, 'R': chess.ROOK, 'N': chess.KNIGHT,
            'B': chess.BISHOP, 'Q': chess.QUEEN, 'K': chess.KING
        }
        
        for symbol, piece_type in piece_symbols.items():
            for color in [chess.WHITE, chess.BLACK]:
                color_name = 'white' if color == chess.WHITE else 'black'
                piece_name = chess.piece_name(piece_type)
                
                # Try to load from assets folder
                image = self._load_piece_image(color_name, piece_name)
                if image is None:
                    # Create Unicode representation
                    image = self._create_unicode_image(piece_type, color)
                
                self.piece_images[(piece_type, color)] = image
    
    def _load_piece_image(self, color: str, piece_name: str) -> Optional[pygame.Surface]:
        """Try to load piece image from assets folder"""
        if not os.path.exists("Chess_game 2.0/assets"):
            return None
            
        naming_patterns = [
            f"{color}_{piece_name}",
            f"{color} {piece_name}",
            f"{color.capitalize()}_{piece_name.capitalize()}",
            f"{color.capitalize()} {piece_name.capitalize()}"
        ]
        
        file_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp']
        
        for pattern in naming_patterns:
            for ext in file_extensions:
                image_filename = f"{pattern}.{ext}"
                image_path = os.path.join('Chess_game 2.0/assets', image_filename)
                
                if os.path.exists(image_path):
                    try:
                        image = pygame.image.load(image_path)
                        return pygame.transform.scale(image, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
                    except Exception as e:
                        print(f"Warning: Could not load image '{image_path}': {e}")
                        continue
        return None
    
    def _create_unicode_image(self, piece_type: int, color: bool) -> pygame.Surface:
        """Create piece image using Unicode chess symbols"""
        unicode_symbols = {
            (chess.KING, chess.WHITE): '♔', (chess.QUEEN, chess.WHITE): '♕',
            (chess.ROOK, chess.WHITE): '♖', (chess.BISHOP, chess.WHITE): '♗',
            (chess.KNIGHT, chess.WHITE): '♘', (chess.PAWN, chess.WHITE): '♙',
            (chess.KING, chess.BLACK): '♚', (chess.QUEEN, chess.BLACK): '♛',
            (chess.ROOK, chess.BLACK): '♜', (chess.BISHOP, chess.BLACK): '♝',
            (chess.KNIGHT, chess.BLACK): '♞', (chess.PAWN, chess.BLACK): '♟'
        }
        
        font_size = min(SQUARE_SIZE - 10, 72)
        font = pygame.font.Font(None, font_size)
        symbol = unicode_symbols[piece_type, color]
        
        surface = pygame.Surface((SQUARE_SIZE - 20, SQUARE_SIZE - 20), pygame.SRCALPHA)
        text_color = (240, 240, 240) if color == chess.WHITE else (40, 40, 40)
        text = font.render(symbol, True, text_color)
        text_rect = text.get_rect(center=(surface.get_width()//2, surface.get_height()//2))
        
        # Add shadow for white pieces
        if color == chess.WHITE:
            shadow = font.render(symbol, True, (100, 100, 100))
            shadow_rect = text_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            surface.blit(shadow, shadow_rect)
        
        surface.blit(text, text_rect)
        return surface
    
    def get_piece_image(self, piece: chess.Piece) -> pygame.Surface:
        """Get the image for a chess piece"""
        return self.piece_images.get((piece.piece_type, piece.color))
    
    def draw_piece(self, surface: pygame.Surface, piece: chess.Piece, x: int, y: int):
        """Draw a piece at the specified position"""
        image = self.get_piece_image(piece)
        if image:
            surface.blit(image, (x + 10, y + 10))

class ChessGameLogic:
    """Wrapper around python-chess with additional game tracking"""
    
    def __init__(self):
        self.board = chess.Board()
        self.selected_square = None
        self.move_history = []
        self.piece_stats = self._init_piece_stats()
        self.captured_pieces = {chess.WHITE: [], chess.BLACK: []}
        self.game_start_time = pygame.time.get_ticks()
    
    def _init_piece_stats(self) -> Dict:
        """Initialize piece movement statistics"""
        stats = {}
        for color in [chess.WHITE, chess.BLACK]:
            stats[color] = {}
            for piece_type in [chess.PAWN, chess.ROOK, chess.KNIGHT, 
                             chess.BISHOP, chess.QUEEN, chess.KING]:
                stats[color][piece_type] = {'moves': 0, 'captures': 0}
        return stats
    
    def pos_to_square(self, row: int, col: int) -> chess.Square:
        """Convert board position to chess.Square"""
        return chess.square(col, 7 - row)
    
    def square_to_pos(self, square: chess.Square) -> Tuple[int, int]:
        """Convert chess.Square to board position"""
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        return (7 - rank, file)
    
    def get_piece_at(self, row: int, col: int) -> Optional[chess.Piece]:
        """Get piece at board position"""
        if 0 <= row < 8 and 0 <= col < 8:
            square = self.pos_to_square(row, col)
            return self.board.piece_at(square)
        return None
    
    def get_legal_moves_from_square(self, square: chess.Square) -> List[chess.Square]:
        """Get legal moves from a specific square"""
        legal_moves = []
        for move in self.board.legal_moves:
            if move.from_square == square:
                legal_moves.append(move.to_square)
        return legal_moves
    
    def make_move(self, from_square: chess.Square, to_square: chess.Square, promotion_piece: Optional[int] = None) -> Optional[chess.Move]:
        """Make a move if it's legal"""
        # Find the exact move (handling promotions)
        move = None
        for legal_move in self.board.legal_moves:
            if legal_move.from_square == from_square and legal_move.to_square == to_square:
                if legal_move.promotion is not None:
                    if promotion_piece is not None and legal_move.promotion == promotion_piece:
                        move = legal_move
                        break
                else:
                    move = legal_move
                    break
        
        if move is None:
            return None
        
        # Record the move and update statistics
        moving_piece = self.board.piece_at(from_square)
        captured_piece = self.board.piece_at(to_square)
        
        if moving_piece:
            self.piece_stats[moving_piece.color][moving_piece.piece_type]['moves'] += 1
            
            if captured_piece:
                self.piece_stats[moving_piece.color][moving_piece.piece_type]['captures'] += 1
                self.captured_pieces[captured_piece.color].append(captured_piece)
        
        # Make the move
        self.board.push(move)
        self.move_history.append(move)
        
        return move
    
    def handle_click(self, row: int, col: int, ui: 'GameUI') -> Tuple[bool, Optional[chess.Move]]:
        if self.board.is_game_over():
            return False, None
    
        square = self.pos_to_square(row, col)
        
        if self.selected_square is None:
            # Select a square if it has a piece of the current player
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                return True, None
        else:
            # Check if the move is a pawn promotion
            piece = self.board.piece_at(self.selected_square)
            promotion_piece = None
            if piece and piece.piece_type == chess.PAWN:
                # Check if the move is to the promotion rank
                to_rank = chess.square_rank(square)
                if (self.board.turn == chess.WHITE and to_rank == 7) or (self.board.turn == chess.BLACK and to_rank == 0):
                    # Convert board coordinates to pixel coordinates for dialog positioning
                    to_row, to_col = self.square_to_pos(square)
                    x = to_col * SQUARE_SIZE
                    y = to_row * SQUARE_SIZE
                    promotion_piece = ui.choose_promotion_piece(WIN, self.board.turn, x, y)
            
            # Try to make a move
            move = self.make_move(self.selected_square, square, promotion_piece)
            self.selected_square = None
            
            if move:
                return True, move
            else:
                # Reselect if clicking on own piece
                piece = self.board.piece_at(square)
                if piece and piece.color == self.board.turn:
                    self.selected_square = square
                    return True, None
        
        return False, None
    
    def get_game_state(self) -> str:
        """Get current game state"""
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            return f"Checkmate! {winner} wins!"
        elif self.board.is_stalemate():
            return "Stalemate - Draw!"
        elif self.board.is_insufficient_material():
            return "Draw - Insufficient material!"
        elif self.board.is_seventyfive_moves():
            return "Draw - 75 move rule!"
        elif self.board.is_fivefold_repetition():
            return "Draw - Fivefold repetition!"
        elif self.board.is_check():
            return "Check!"
        else:
            return "Game in progress"
    
    def reset(self):
        """Reset the game"""
        self.board = chess.Board()
        self.selected_square = None
        self.move_history = []
        self.piece_stats = self._init_piece_stats()
        self.captured_pieces = {chess.WHITE: [], chess.BLACK: []}
        self.game_start_time = pygame.time.get_ticks()

class GameUI:
    """User interface management"""
    
    def __init__(self, game_logic: ChessGameLogic, piece_renderer: PieceRenderer, 
                 sound_engine: SoundEngine):
        self.game_logic = game_logic
        self.piece_renderer = piece_renderer
        self.sound_engine = sound_engine
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
    
    def draw_board(self, surface: pygame.Surface):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)
        
        # Draw coordinates
        coord_font = pygame.font.Font(None, 20)
        for i in range(8):
            # Files (a-h)
            file_letter = chr(ord('a') + i)
            text = coord_font.render(file_letter, True, BLACK)
            surface.blit(text, (i * SQUARE_SIZE + 5, BOARD_HEIGHT - 20))
            
            # Ranks (1-8)
            rank_number = str(8 - i)
            text = coord_font.render(rank_number, True, BLACK)
            surface.blit(text, (5, i * SQUARE_SIZE + 5))
    
    def draw_highlights(self, surface: pygame.Surface):
        """Draw square highlights"""
        # Highlight last move
        if self.game_logic.move_history:
            last_move = self.game_logic.move_history[-1]
            for square in [last_move.from_square, last_move.to_square]:
                row, col = self.game_logic.square_to_pos(square)
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight_surface.fill(LAST_MOVE_COLOR)
                surface.blit(highlight_surface, rect)
        
        # Highlight selected square
        if self.game_logic.selected_square is not None:
            row, col = self.game_logic.square_to_pos(self.game_logic.selected_square)
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(SELECTED_COLOR)
            surface.blit(highlight_surface, rect)
            
            # Highlight valid moves
            legal_moves = self.game_logic.get_legal_moves_from_square(self.game_logic.selected_square)
            for move_square in legal_moves:
                move_row, move_col = self.game_logic.square_to_pos(move_square)
                center_x = move_col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = move_row * SQUARE_SIZE + SQUARE_SIZE // 2
                
                target_piece = self.game_logic.board.piece_at(move_square)
                if target_piece:  # Capture move
                    pygame.draw.circle(surface, (255, 0, 0), (center_x, center_y), SQUARE_SIZE // 3, 4)
                else:  # Regular move
                    pygame.draw.circle(surface, (0, 255, 0), (center_x, center_y), 12)
        
        # Highlight king in check
        if self.game_logic.board.is_check():
            king_square = self.game_logic.board.king(self.game_logic.board.turn)
            if king_square is not None:
                row, col = self.game_logic.square_to_pos(king_square)
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight_surface.fill(CHECK_COLOR)
                surface.blit(highlight_surface, rect)
    
    def draw_pieces(self, surface: pygame.Surface):
        """Draw all pieces on the board"""
        for square in chess.SQUARES:
            piece = self.game_logic.board.piece_at(square)
            if piece:
                row, col = self.game_logic.square_to_pos(square)
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                self.piece_renderer.draw_piece(surface, piece, x, y)
    
    def draw_info_panel(self, surface: pygame.Surface):
        """Draw the information panel"""
        panel_rect = pygame.Rect(BOARD_WIDTH, 0, INFO_PANEL_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(surface, PANEL_BG, panel_rect)
        
        y_offset = 20
        
        # Game title
        title = self.font_large.render("Chess Game", True, TEXT_PRIMARY)
        surface.blit(title, (BOARD_WIDTH + 20, y_offset))
        y_offset += 60
        
        # Current turn
        turn_text = f"Turn: {'White' if self.game_logic.board.turn == chess.WHITE else 'Black'}"
        turn_surface = self.font_medium.render(turn_text, True, TEXT_PRIMARY)
        surface.blit(turn_surface, (BOARD_WIDTH + 20, y_offset))
        y_offset += 40
        
        # Game status
        status_text = self.game_logic.get_game_state()
        status_color = TEXT_PRIMARY
        if "Check" in status_text:
            status_color = (255, 100, 100)
        elif "wins" in status_text or "Draw" in status_text:
            status_color = (255, 50, 50)
        
        # Wrap long status text
        if len(status_text) > 20:
            words = status_text.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line + word) < 20:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())
            
            for line in lines:
                status_surface = self.font_medium.render(line, True, status_color)
                surface.blit(status_surface, (BOARD_WIDTH + 20, y_offset))
                y_offset += 25
        else:
            status_surface = self.font_medium.render(status_text, True, status_color)
            surface.blit(status_surface, (BOARD_WIDTH + 20, y_offset))
            y_offset += 40
        
        y_offset += 10
        
        # Move count and game time
        move_count = len(self.game_logic.move_history)
        move_text = f"Moves: {move_count}"
        move_surface = self.font_small.render(move_text, True, TEXT_SECONDARY)
        surface.blit(move_surface, (BOARD_WIDTH + 20, y_offset))
        y_offset += 20
        
        game_time = (pygame.time.get_ticks() - self.game_logic.game_start_time) // 1000
        time_text = f"Time: {game_time // 60:02d}:{game_time % 60:02d}"
        time_surface = self.font_small.render(time_text, True, TEXT_SECONDARY)
        surface.blit(time_surface, (BOARD_WIDTH + 20, y_offset))
        y_offset += 30
        
        # Board evaluation (simple material count)
        material_balance = self._calculate_material_balance()
        if material_balance > 0:
            eval_text = f"White +{material_balance}"
        elif material_balance < 0:
            eval_text = f"Black +{abs(material_balance)}"
        else:
            eval_text = "Equal material"
        
        eval_surface = self.font_small.render(eval_text, True, TEXT_SECONDARY)
        surface.blit(eval_surface, (BOARD_WIDTH + 20, y_offset))
        y_offset += 30
        
        # Recent moves
        moves_title = self.font_medium.render("Recent Moves:", True, TEXT_PRIMARY)
        surface.blit(moves_title, (BOARD_WIDTH + 20, y_offset))
        y_offset += 30
        
        recent_moves = self.game_logic.move_history[-8:]  # Show last 8 moves
        for i, move in enumerate(recent_moves):
            move_num = len(self.game_logic.move_history) - len(recent_moves) + i + 1
            try:
                # Create a temporary board to get SAN notation
                temp_board = chess.Board()
                for m in self.game_logic.move_history[:move_num-1]:
                    temp_board.push(m)
                move_text = f"{move_num}. {temp_board.san(move)}"
            except:
                move_text = f"{move_num}. {move.uci()}"
                
            move_surface = self.font_small.render(move_text, True, TEXT_SECONDARY)
            surface.blit(move_surface, (BOARD_WIDTH + 30, y_offset))
            y_offset += 18
        
        # Captured pieces
        y_offset += 20
        captured_title = self.font_medium.render("Captured:", True, TEXT_PRIMARY)
        surface.blit(captured_title, (BOARD_WIDTH + 20, y_offset))
        y_offset += 30
        
        for color in [chess.WHITE, chess.BLACK]:
            if self.game_logic.captured_pieces[color]:
                color_name = "White" if color == chess.WHITE else "Black"
                pieces_text = ", ".join([chess.piece_name(p.piece_type) for p in self.game_logic.captured_pieces[color]])
                full_text = f"{color_name}: {pieces_text}"
                
                # Wrap text if too long
                if len(full_text) > 25:
                    full_text = full_text[:25] + "..."
                
                captured_surface = self.font_small.render(full_text, True, TEXT_SECONDARY)
                surface.blit(captured_surface, (BOARD_WIDTH + 30, y_offset))
                y_offset += 18
        
        # Controls
        y_offset = WINDOW_HEIGHT - 140
        controls_title = self.font_small.render("Controls:", True, ACCENT_COLOR)
        surface.blit(controls_title, (BOARD_WIDTH + 20, y_offset))
        y_offset += 20
        
        controls_text = [
            "Click: Select/Move",
            "R: Reset Game",
            "H: Show History",
            "F: Flip Board",
            "S: Toggle Sound",
            "ESC: Quit"
        ]
        
        for control in controls_text:
            control_surface = self.font_small.render(control, True, TEXT_SECONDARY)
            surface.blit(control_surface, (BOARD_WIDTH + 30, y_offset))
            y_offset += 15

    def choose_promotion_piece(self, surface: pygame.Surface, color: bool, x: int, y: int) -> int:
        promotion_options = [
            (chess.QUEEN, "Queen"),
            (chess.ROOK, "Rook"),
            (chess.BISHOP, "Bishop"),
            (chess.KNIGHT, "Knight")
        ]

        button_width = 80
        button_height = 40
        button_space = 10
        total_width = (button_width * 2) + button_space
        total_height = (button_height * 2) + button_space

        dialog_x = min(max(x, 0), BOARD_WIDTH - total_width)
        dialog_y = min(max(y, 0), BOARD_HEIGHT - total_height)

        dialog_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        dialog_surface.fill((50, 50, 50, 200))  # Semi-transparent background

        buttons = []
        # Define font before using it
        font = pygame.font.Font(None, 24)
        for i, (piece_type, piece_name) in enumerate(promotion_options):
            row = i // 2
            col = i % 2
            button_x = col * (button_width + button_space)
            button_y = row * (button_height + button_space)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            buttons.append((button_rect, piece_type, piece_name))

            pygame.draw.rect(dialog_surface, (100, 100, 100), button_rect)
            text = font.render(piece_name, True, (255, 255, 255))
            text_rect = text.get_rect(center=button_rect.center)
            dialog_surface.blit(text, text_rect)

        surface.blit(dialog_surface, (dialog_x, dialog_y))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    adjusted_pos = (mouse_pos[0] - dialog_x, mouse_pos[1] - dialog_y)
                    for button_rect, piece_type, piece_name in buttons:
                        if button_rect.collidepoint(adjusted_pos):
                            return piece_type   
                elif event.type == pygame.KEYDOWN:
                    key_map = {
                        pygame.K_q: chess.QUEEN,
                        pygame.K_r: chess.ROOK,
                        pygame.K_b: chess.BISHOP,
                        pygame.K_n: chess.KNIGHT  # Fixed: was K_k, should be K_n for knight
                    }
                    if event.key in key_map:
                        return key_map[event.key]
    
    def _calculate_material_balance(self) -> int:
        """Calculate material balance (positive = white advantage)"""
        piece_values = {
            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
        }
        
        balance = 0
        for square in chess.SQUARES:
            piece = self.game_logic.board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                balance += value if piece.color == chess.WHITE else -value
        
        return balance
    
    def draw(self, surface: pygame.Surface):
        """Draw the complete game interface"""
        surface.fill(WHITE)
        self.draw_board(surface)
        self.draw_highlights(surface)
        self.draw_pieces(surface)
        self.draw_info_panel(surface)

class ChessGame:
    """Main game controller"""
    
    def __init__(self):
        self.game_logic = ChessGameLogic()
        self.piece_renderer = PieceRenderer()
        self.sound_engine = SoundEngine()
        self.ui = GameUI(self.game_logic, self.piece_renderer, self.sound_engine)
        self.clock = pygame.time.Clock()
        self.running = True
        self.board_flipped = False
        
        # Print setup information
        self._print_setup_info()
    
    def _print_setup_info(self):
        """Print game setup information"""
        print("Advanced Chess Game with python-chess library")
        print(f"python-chess version: {chess.__version__}")
        
        assets_path = "Chess_game 2.0/assets"
        if os.path.exists(assets_path) and os.path.isdir(assets_path):
            print(f"Assets folder found at: {os.path.abspath(assets_path)}")
            image_files = [f for f in os.listdir(assets_path) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            if image_files:
                print(f"Found {len(image_files)} piece images")
            else:
                print("No images found, using Unicode symbols")
        else:
            print("No assets folder found, using Unicode symbols")
        print("-" * 50)
    
    def handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if event.pos[0] < BOARD_WIDTH:  # Click on board
                        x, y = event.pos
                        col = x // SQUARE_SIZE
                        row = y // SQUARE_SIZE if not self.board_flipped else 7 - (y // SQUARE_SIZE)
                        
                        if self.board_flipped:
                            row, col = 7 - row, 7 - col
                        
                        if 0 <= row < 8 and 0 <= col < 8:
                            clicked, move = self.game_logic.handle_click(row, col, self.ui)
                            
                            if move:
                                self._play_move_sound(move)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_h:
                    self.print_game_analysis()
                elif event.key == pygame.K_f:
                    self.board_flipped = not self.board_flipped
                    print(f"Board {'flipped' if self.board_flipped else 'normal'}")
                elif event.key == pygame.K_s:
                    self.toggle_sound()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def _play_move_sound(self, move: chess.Move):
        """Play appropriate sound for a move"""
        if self.game_logic.board.is_checkmate():
            self.sound_engine.play('checkmate')
        elif self.game_logic.board.is_check():
            self.sound_engine.play('check')
        elif move.promotion:
            self.sound_engine.play('promotion')
        elif self.game_logic.board.is_castling(move):
            self.sound_engine.play('castle')
        elif self.game_logic.board.is_capture(move):
            self.sound_engine.play('capture')
        else:
            self.sound_engine.play('move')
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.game_logic.reset()
        print("Game reset!")
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.sound_engine.enabled = not self.sound_engine.enabled
        status = "enabled" if self.sound_engine.enabled else "disabled"
        print(f"Sound {status}")
    
    def print_game_analysis(self):
        """Print detailed game analysis"""
        board = self.game_logic.board

        print(f"\nFEN: {board.fen()}")
        print(f"Legal Moves: {[move.uci() for move in board.legal_moves]}")
        
        turn_color = "white" if board.turn else "black"

        if board.is_check():
            checking_color = "black" if board.turn else "white"
            print(f"Current position: {checking_color} has {turn_color} king in check")
        
        if board.is_checkmate():
            print(f"{turn_color.capitalize()} is in checkmate!")
        elif board.is_stalemate():
            print("Game is a stalemate.")
        elif board.is_insufficient_material():
            print("Draw due to insufficient material.")
        elif board.is_seventyfive_moves():
            print("Draw by 75-move rule.")
        elif board.is_fivefold_repetition():
            print("Draw by fivefold repetition.")
        elif board.is_variant_draw():
            print("Draw (variant rule).")

    def run(self):
        """Main game loop"""
        print("Advanced Chess Game Started!")
        print("Using python-chess library for game logic")
        print("Controls:")
        print("  - Click to select and move pieces")
        print("  - R: Reset game")
        print("  - H: Show complete game analysis")
        print("  - F: Flip board view")
        print("  - S: Toggle sound")
        print("  - ESC: Quit game")
        print("-" * 50)
        
        while self.running:
            self.handle_events()
            
            # Handle board flipping for display
            if self.board_flipped:
                # Create a flipped surface
                temp_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                self.ui.draw(temp_surface)
                
                # Flip the board portion
                board_surface = temp_surface.subsurface((0, 0, BOARD_WIDTH, BOARD_HEIGHT))
                flipped_board = pygame.transform.rotate(board_surface, 180)
                
                WIN.fill(WHITE)
                WIN.blit(flipped_board, (0, 0))
                # Keep info panel normal
                info_panel = temp_surface.subsurface((BOARD_WIDTH, 0, INFO_PANEL_WIDTH, WINDOW_HEIGHT))
                WIN.blit(info_panel, (BOARD_WIDTH, 0))
            else:
                self.ui.draw(WIN)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

def main():
    """Initialize and run the chess game"""
    try:
        # Check if python-chess is installed
        import chess
        import chess.pgn
        print(f"python-chess library version {chess.__version__} loaded successfully")
    except ImportError as e:
        print("Error: python-chess library not found!")
        print("Please install it using: pip install python-chess")
        print("This library is required for the chess logic.")
        sys.exit(1)
    
    try:
        game = ChessGame()
        game.run()
    except Exception as e:
        print(f"Error running chess game: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()  