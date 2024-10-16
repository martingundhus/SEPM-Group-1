import random
import math
from copy import deepcopy

# Minimax algorithm implementation
def minimax(board, depth, is_maximizing, alpha, beta, is_first_move):
    # Base cases: terminal state (win/loss, draw, or depth limit reached)
    if board.has_path(1):  # AI has a winning path
        return float('inf')
    if board.has_path(0):  # Player has a winning path
        return float('-inf')
    if board.is_stalemate(1) or depth == 0:
        return board.evaluate()  # Evaluate current board if depth limit is reached

    if is_maximizing:
        # AI's turn (Maximizer)
        max_eval = -math.inf
        if is_first_move:
            valid_moves = board.get_valid_moves(0)  # Get player moves
        else:
            valid_moves = board.get_valid_moves(1)  # Get AI moves
        for move in valid_moves:
            new_board = simulate_move(board, move, 1)
            evaluation = minimax(new_board, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return max_eval
    else:
        # Player's turn (Minimizer)
        min_eval = math.inf
        if is_first_move:
            valid_moves = board.get_valid_moves(1)  # Get AI moves
        else:
            valid_moves = board.get_valid_moves(0)  # Get player moves
        for move in valid_moves:
            new_board = simulate_move(board, move, 0)
            evaluation = minimax(new_board, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return min_eval

# Function to simulate a move and return a new board state
def simulate_move(board, move, owner):
    new_board = deepcopy(board)  # Deep copy the board to simulate the move
    new_board.apply_action(move, owner)  # Apply the move
    return new_board

# AI action selection for different levels
def get_action_level1(moves):
    # Random selection for easy difficulty (placeholder)
    return random.choice(moves)

def get_action_level2(board, player):
    # Medium difficulty with shallow minimax
    best_move = None
    best_score = -math.inf
    is_first_move = False

    if board.turns < 2:
        piece_color = 1 - player
        is_first_move = True

    for move in board.get_valid_moves(piece_color):
        new_board = simulate_move(board, move, 1)
        score = minimax(new_board, depth=2, is_maximizing= not bool(player), alpha=-math.inf, beta=math.inf, is_first_move=is_first_move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def get_action_level3(board, player):
    # Hard difficulty with deeper minimax
    best_move = None
    best_score = -math.inf
    is_first_move = False

    if board.turns < 2:
        piece_color = 1 - player
        is_first_move = True
    
    for move in board.get_valid_moves(piece_color):
        new_board = simulate_move(board, move, 1)
        score = minimax(new_board, depth=4, is_maximizing= not bool(player), alpha=-math.inf, beta=math.inf, is_first_move=is_first_move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move



