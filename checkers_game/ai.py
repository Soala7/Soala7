import pygame
import copy

# Minimax AI with alpha-beta pruning
def minimax(position, depth, max_player, game, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or position.winner() is not None:
        return evaluate(position), position

    if max_player:  # AI's turn (Black)
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, (0, 0, 0), game):  # Black pieces
            evaluation = minimax(move, depth - 1, False, game, alpha, beta)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:  # Human's turn (Red)
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, (255, 0, 0), game):  # Red pieces
            evaluation = minimax(move, depth - 1, True, game, alpha, beta)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval, best_move


def evaluate(board):
    """Simple evaluation: pieces + king advantage"""
    return board.black_left - board.red_left + (board.black_kings * 0.5 - board.red_kings * 0.5)


def simulate_move(piece, move, board, game, skipped):
    board.move(piece, move[0], move[1])
    if skipped:
        board.remove(skipped)
    return board


def get_all_moves(board, color, game):
    moves = []

    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece != 0 and piece.color == color:
                valid_moves = game.get_valid_moves(piece)
                for move, skipped in valid_moves.items():
                    temp_board = copy.deepcopy(board)
                    temp_piece = temp_board.get_piece(row, col)
                    new_board = simulate_move(temp_piece, move, temp_board, game, skipped)
                    moves.append(new_board)

    return moves
