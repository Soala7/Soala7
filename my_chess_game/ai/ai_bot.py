import chess
import chess.engine
import random
import time
from typing import Optional, Dict, Set, Tuple
from collections import defaultdict

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
        self.move_history: Dict[str, int] = defaultdict(int)
        self.position_history: Set[str] = set()
        self.last_positions = []
        
        # Transposition table for memoization
        self.transposition_table = {}
        self.max_table_size = 10000
        
    def get_best_move(self, board: chess.Board, max_time: float = 0.5) -> chess.Move:
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
        for move in legal_moves:
            score = self._quick_move_score(board, move)
            # Penalize moves that lead to repetition
            if self._would_repeat_position(board, move):
                score -= 500
            move_scores.append((score, move))
        
        # Sort moves by quick evaluation (best first)
        move_scores.sort(reverse=True)
        ordered_moves = [move for _, move in move_scores]
        
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
        move_scores = [(self._quick_move_score(board, move), move) for move in legal_moves]
        move_scores.sort(reverse=maximizing)
        ordered_moves = [move for _, move in move_scores[:10]]  # Limit for speed
        
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
        board.push(chess.Move.null())  # Pass turn
        if not board.is_game_over():
            opponent_mobility = len(list(board.legal_moves))
        else:
            opponent_mobility = 0
        board.pop()
        
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

class FastChessGame:
    """Fast chess game with improved AI"""
    
    def __init__(self):
        self.board = chess.Board()
        self.ai = FastIntermediateChessAI()
        self.ai_color = chess.BLACK
        self.human_color = chess.WHITE
        self.last_move = None
        self.game_over = False
        self.move_times = []
    
    def make_human_move(self, move: chess.Move) -> bool:
        """Make a move for the human player"""
        if self.game_over or self.board.turn != self.human_color:
            return False
        
        if move in self.board.legal_moves:
            self.board.push(move)
            self.last_move = move
            self._check_game_over()
            return True
        return False
    
    def make_ai_move(self, max_time: float = 0.5) -> Optional[chess.Move]:
        """Have the AI make its move with time limit"""
        if self.game_over or self.board.turn != self.ai_color:
            return None
        
        start_time = time.time()
        move = self.ai.get_best_move(self.board, max_time)
        move_time = time.time() - start_time
        
        if move:
            self.board.push(move)
            self.last_move = move
            self.move_times.append(move_time)
            self._check_game_over()
            
        return move
    
    def _check_game_over(self):
        """Check if the game is over"""
        self.game_over = self.board.is_game_over()
    
    def get_game_state(self) -> str:
        """Get current game state description"""
        if self.board.is_checkmate():
            return "Checkmate! You win!" if self.board.turn == self.ai_color else "Checkmate! AI wins!"
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
        self.ai = FastIntermediateChessAI()  # Reset AI state
        self.last_move = None
        self.game_over = False
        self.move_times = []

# Example usage
if __name__ == "__main__":
    game = FastChessGame()
    
    # Example game loop
    while not game.game_over:
        print(f"\nCurrent position:\n{game.board}")
        print(f"Game state: {game.get_game_state()}")
        
        if game.board.turn == game.human_color:
            # Human move (you would get this from your UI)
            move_str = input("Enter your move (e.g., e2e4): ")
            try:
                move = chess.Move.from_uci(move_str)
                if game.make_human_move(move):
                    print(f"You played: {move}")
                else:
                    print("Invalid move!")
                    continue
            except:
                print("Invalid move format!")
                continue
        else:
            # AI move
            print("AI is thinking...")
            move = game.make_ai_move(max_time=1.0)  # 1 second max
            if move:
                print(f"AI played: {move}")
    
    print(f"\nGame over! {game.get_game_state()}")
    print(f"Average AI move time: {game.get_average_move_time():.3f} seconds")