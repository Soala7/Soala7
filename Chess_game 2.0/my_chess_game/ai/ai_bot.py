import pygame
import chess
import random
import time
import os
import sys
from typing import Optional, Dict, Tuple, List

# ---------- CONFIG ----------
WINDOW_W = 880   # board 640 + sidebar 240
BOARD_SIZE = 640
SQUARE = BOARD_SIZE // 8
SIDEBAR = WINDOW_W - BOARD_SIZE
WINDOW_H = BOARD_SIZE
FPS = 60

AI_DEPTH = 3   # default AI strength

# ---------- COLORS ----------
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT = (255, 255, 0, 100)
LEGAL = (0, 200, 0, 90)
LAST = (255, 165, 0, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SIDEBAR_BG = (245, 245, 245)
BUTTON = (70, 130, 180)
BUTTON_H = (100, 149, 237)

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Smart Fast Chess AI")
clock = pygame.time.Clock()

# Fonts
F_LARGE = pygame.font.Font(None, 36)
F_MED = pygame.font.Font(None, 26)
F_SMALL = pygame.font.Font(None, 20)
UNICODE_FONT = pygame.font.Font(None, SQUARE - 10)

# ---------- IMAGE LOADING ----------
PIECE_FILES = {
    'P': ('white', 'pawn'), 'N': ('white', 'knight'), 'B': ('white', 'bishop'), 'R': ('white', 'rook'),
    'Q': ('white', 'queen'), 'K': ('white', 'king'),
    'p': ('black', 'pawn'), 'n': ('black', 'knight'), 'b': ('black', 'bishop'), 'r': ('black', 'rook'),
    'q': ('black', 'queen'), 'k': ('black', 'king'),
}
PIECES_IMG: Dict[str, Optional[pygame.Surface]] = {}
USE_IMAGES = True

def try_load_image(patterns: List[str], exts=('png','jpg','jpeg','bmp','gif')) -> Optional[pygame.Surface]:
    for p in patterns:
        for ext in exts:
            path = os.path.join('Chess_game 2.0/assets', f"{p}.{ext}")
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    return pygame.transform.smoothscale(img, (SQUARE, SQUARE))
                except:
                    continue
    return None

for sym, (color, name) in PIECE_FILES.items():
    patterns = [
        f"{color}_{name}", f"{color} {name}", f"{color}{name}", f"{color}{name.capitalize()}",
        f"{color.capitalize()}_{name}", f"{color.capitalize()} {name}", f"{color}_{name.capitalize()}",
    ]
    img = try_load_image(patterns)
    if img is None:
        USE_IMAGES = False
        break
    else:
        PIECES_IMG[sym] = img

UNICODE = {'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
           'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'}

# ---------- EVALUATION ----------
PIECE_VALUE = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
}

PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]
KNIGHT_TABLE = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50
]
TT = {}

def evaluate_board(board: chess.Board) -> int:
    if board.is_checkmate():
        return -999999 if board.turn == chess.WHITE else 999999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    score = 0
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            val = PIECE_VALUE[piece.piece_type]
            if piece.piece_type == chess.PAWN:
                val += PAWN_TABLE[sq if piece.color == chess.WHITE else chess.square_mirror(sq)]
            elif piece.piece_type == chess.KNIGHT:
                val += KNIGHT_TABLE[sq if piece.color == chess.WHITE else chess.square_mirror(sq)]
            score += val if piece.color == chess.WHITE else -val
    score += len(list(board.legal_moves)) * (3 if board.turn == chess.WHITE else -3)
    return score

# ---------- AI ----------
def order_moves(board: chess.Board, moves: List[chess.Move]) -> List[chess.Move]:
    scored = []
    for m in moves:
        score = 0
        if board.is_capture(m):
            captured = board.piece_at(m.to_square)
            mover = board.piece_at(m.from_square)
            if captured:
                score += PIECE_VALUE[captured.piece_type] - (PIECE_VALUE[mover.piece_type] // 10)
        if m.promotion:
            score += 900
        score += random.random() * 0.1
        scored.append((score, m))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored]

def negamax(board: chess.Board, depth: int, alpha: int, beta: int, color: int) -> int:
    key = (board.board_fen(), depth, board.turn)
    if key in TT:
        return TT[key]
    if depth == 0 or board.is_game_over():
        val = color * evaluate_board(board)
        TT[key] = val
        return val
    maxv = -9999999
    for m in order_moves(board, list(board.legal_moves))[:60]:
        board.push(m)
        val = -negamax(board, depth - 1, -beta, -alpha, -color)
        board.pop()
        if val > maxv:
            maxv = val
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    TT[key] = maxv
    return maxv

def ai_best_move(board: chess.Board, depth=AI_DEPTH) -> Optional[chess.Move]:
    best, best_score = None, -9999999
    for m in order_moves(board, list(board.legal_moves))[:120]:
        board.push(m)
        score = -negamax(board, depth - 1, -10000000, 10000000, -1)
        board.pop()
        if score > best_score:
            best_score, best = score, m
    return best

# ---------- UI Helpers ----------
def square_to_screen(square: int, flip=False) -> Tuple[int, int]:
    col = chess.square_file(square)
    row = 7 - chess.square_rank(square)
    if flip:
        col, row = 7 - col, 7 - row
    return col * SQUARE, row * SQUARE

def mouse_to_square(pos: Tuple[int, int], flip=False) -> Optional[int]:
    x, y = pos
    if x >= BOARD_SIZE:
        return None
    col, row = x // SQUARE, y // SQUARE
    if flip:
        col, row = 7 - col, 7 - row
    return chess.square(col, 7 - row)

# ---------- Dialogs ----------
def choose_color_dialog() -> chess.Color:
    title = F_LARGE.render("Choose Your Color", True, BLACK)
    white_rect = pygame.Rect(100, 250, 180, 80)
    black_rect = pygame.Rect(360, 250, 180, 80)
    while True:
        mx, my = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if white_rect.collidepoint(mx, my):
                    return chess.WHITE
                if black_rect.collidepoint(mx, my):
                    return chess.BLACK
        for y in range(WINDOW_H):
            col = (240 - y//4, 240 - y//4, 240 - y//4)
            pygame.draw.line(screen, col, (0, y), (WINDOW_W, y))
        screen.blit(title, (BOARD_SIZE//2 - title.get_width()//2, 150))
        for rect, label in [(white_rect, "Play as White"), (black_rect, "Play as Black")]:
            hover = rect.collidepoint(mx, my)
            pygame.draw.rect(screen, BUTTON_H if hover else BUTTON, rect, border_radius=10)
            text = F_MED.render(label, True, WHITE)
            screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))
        pygame.display.flip()
        clock.tick(30)

# ---------- Draw Functions ----------assets
def draw_board(selected: Optional[int], legal_moves: List[chess.Move], last_move: Optional[chess.Move], flip=False):
    pygame.draw.rect(screen, (100, 100, 100), (2, 2, BOARD_SIZE+4, BOARD_SIZE+4))
    for r in range(8):
        for c in range(8):
            x, y = c*SQUARE, r*SQUARE
            color = LIGHT if (r+c) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (x, y, SQUARE, SQUARE))
    if last_move:
        for sq in [last_move.from_square, last_move.to_square]:
            sx, sy = square_to_screen(sq, flip)
            surf = pygame.Surface((SQUARE, SQUARE), pygame.SRCALPHA)
            surf.fill(LAST)
            screen.blit(surf, (sx, sy))
    if selected is not None:
        sx, sy = square_to_screen(selected, flip)
        surf = pygame.Surface((SQUARE, SQUARE), pygame.SRCALPHA)
        surf.fill(HIGHLIGHT)
        screen.blit(surf, (sx, sy))
    for m in legal_moves:
        sx, sy = square_to_screen(m.to_square, flip)
        surf = pygame.Surface((SQUARE, SQUARE), pygame.SRCALPHA)
        surf.fill(LEGAL)
        screen.blit(surf, (sx, sy))
        pygame.draw.circle(screen, (0, 120, 0), (sx + SQUARE//2, sy + SQUARE//2), SQUARE//8)

def draw_pieces(board: chess.Board, flip=False):
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if not piece: continue
        x, y = square_to_screen(sq, flip)
        sym = piece.symbol()
        if USE_IMAGES:
            screen.blit(PIECES_IMG[sym], (x, y))
        else:
            txt = UNICODE_FONT.render(UNICODE[sym], True, (0, 0, 0))
            rect = txt.get_rect(center=(x + SQUARE//2, y + SQUARE//2))
            screen.blit(txt, rect)

def draw_sidebar(board: chess.Board, ai_level: int):
    pygame.draw.rect(screen, SIDEBAR_BG, (BOARD_SIZE, 0, SIDEBAR, WINDOW_H))
    pygame.draw.line(screen, (180, 180, 180), (BOARD_SIZE, 0), (BOARD_SIZE, WINDOW_H), 3)
    y = 30
    screen.blit(F_LARGE.render("♟ Smart Chess AI ♞", True, (50, 50, 50)), (BOARD_SIZE+10, y))
    y += 50
    pygame.draw.line(screen, (200, 200, 200), (BOARD_SIZE+10, y), (BOARD_SIZE+SIDEBAR-10, y), 1)
    y += 20
    t = "White to move" if board.turn == chess.WHITE else "Black to move"
    screen.blit(F_MED.render(t, True, (0, 0, 0)), (BOARD_SIZE+10, y)); y += 30
    screen.blit(F_MED.render(f"AI Depth: {ai_level}", True, (0, 0, 0)), (BOARD_SIZE+10, y)); y += 30
    pygame.draw.line(screen, (200, 200, 200), (BOARD_SIZE+10, y), (BOARD_SIZE+SIDEBAR-10, y), 1); y += 20
    controls = ["Controls:", "• Click piece → Select", "• Click square → Move", "• R: Reset", "• Q: Quit", "• 1–5: AI depth"]
    for c in controls:
        screen.blit(F_SMALL.render(c, True, (40, 40, 40)), (BOARD_SIZE+10, y)); y += 22

# ---------- Promotion Choice UI ----------
def draw_promotion_choices(color: chess.Color, flip: bool) -> List[Tuple[pygame.Rect, int]]:
    """Draws promotion choices and returns list of (rect, piece_type)"""
    choices = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
    rects = []
    base_x = BOARD_SIZE//2 - 2*SQUARE
    base_y = BOARD_SIZE//2 - SQUARE//2
    for i, pt in enumerate(choices):
        x = base_x + i * SQUARE
        y = base_y
        rect = pygame.Rect(x, y, SQUARE, SQUARE)
        rects.append((rect, pt))
        pygame.draw.rect(screen, LIGHT if (i % 2 == 0) else DARK, rect)
        sym = chess.Piece(pt, color).symbol()
        if USE_IMAGES:
            screen.blit(PIECES_IMG[sym], (x, y))
        else:
            txt = UNICODE_FONT.render(UNICODE[sym], True, BLACK)
            rect_txt = txt.get_rect(center=rect.center)
            screen.blit(txt, rect_txt)
    return rects

# ---------- Game Init ----------
player_color = choose_color_dialog()
ai_color = not player_color
board = chess.Board()
selected_sq, legal_moves, last_mv = None, [], None
ai_timer = 0
flip_board = (player_color == chess.BLACK)

if ai_color == chess.WHITE:
    m = ai_best_move(board, depth=AI_DEPTH)
    if m: board.push(m); last_mv = m

promotion_mode = False
promotion_move = None
promotion_rects = []

# ---------- Main Loop ----------
running = True
while running:
    clock.tick(FPS)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_q:
                running = False
            elif ev.key == pygame.K_r:
                board = chess.Board()
                selected_sq, legal_moves, last_mv = None, [], None
                TT.clear()
                promotion_mode = False
                promotion_move = None
                promotion_rects = []
                if ai_color == chess.WHITE:
                    m = ai_best_move(board, depth=AI_DEPTH)
                    if m: board.push(m); last_mv = m
            elif ev.key in (pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5):
                AI_DEPTH = int(ev.unicode) if ev.unicode.isdigit() else AI_DEPTH
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if promotion_mode:
                # Check if player clicked on a promotion piece
                pos = ev.pos
                chosen_piece = None
                for rect, pt in promotion_rects:
                    if rect.collidepoint(pos):
                        chosen_piece = pt
                        break
                if chosen_piece is not None and promotion_move is not None:
                    # Make promotion move with chosen piece
                    move = chess.Move(promotion_move.from_square, promotion_move.to_square, promotion=chosen_piece)
                    if move in board.legal_moves:
                        board.push(move)
                        last_mv = move
                    promotion_mode = False
                    promotion_move = None
                    promotion_rects = []
                    selected_sq, legal_moves = None, []
                    ai_timer = pygame.time.get_ticks() + 150
                continue

            if board.is_game_over():
                continue
            if board.turn != player_color:
                continue
            sq = mouse_to_square(ev.pos, flip_board)
            if sq is None:
                continue
            piece = board.piece_at(sq)

            if selected_sq is None:
                if piece and piece.color == player_color:
                    selected_sq = sq
                    legal_moves = [m for m in board.legal_moves if m.from_square == selected_sq]
                else:
                    selected_sq, legal_moves = None, []
            else:
                attempted = chess.Move(selected_sq, sq)
                moving_piece = board.piece_at(selected_sq)
                if moving_piece and moving_piece.piece_type == chess.PAWN:
                    to_rank = chess.square_rank(sq)
                    # Check if pawn promotion is possible (moving to last rank)
                    if (moving_piece.color == chess.WHITE and to_rank == 7) or (moving_piece.color == chess.BLACK and to_rank == 0):
                        # Enter promotion selection mode
                        promotion_mode = True
                        promotion_move = chess.Move(selected_sq, sq)
                        promotion_rects = draw_promotion_choices(moving_piece.color, flip_board)
                        continue
                if attempted in board.legal_moves:
                    board.push(attempted)
                    last_mv = attempted
                    selected_sq, legal_moves = None, []
                    if len(TT) > 100000:
                        TT.clear()
                    ai_timer = pygame.time.get_ticks() + 150
                else:
                    if piece and piece.color == player_color:
                        selected_sq = sq
                        legal_moves = [m for m in board.legal_moves if m.from_square == selected_sq]
                    else:
                        selected_sq, legal_moves = None, []

    if not promotion_mode and board.turn == ai_color and not board.is_game_over():
        now = pygame.time.get_ticks()
        if ai_timer and now >= ai_timer:
            ai_timer = 0
            m = ai_best_move(board, depth=AI_DEPTH)
            if m:
                board.push(m)
                last_mv = m

    # Draw everything
    draw_board(selected_sq, legal_moves, last_mv, flip_board)
    draw_pieces(board, flip_board)
    draw_sidebar(board, AI_DEPTH)
    if promotion_mode:
        promotion_rects = draw_promotion_choices(board.turn, flip_board)
    pygame.display.flip()

pygame.quit()
sys.exit()
