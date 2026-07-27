"""
Move generation with move ordering
Author: Rajesh Thapa (bokshi)
"""

from .constants import *
from .bitboard import *

def generate_moves(board):
    """Generate all legal moves for the current side"""
    moves = []
    color = board.side_to_move
    enemy = 1 - color
    
    pieces = board.color_bitboards[color]
    while pieces:
        lsb = pieces & -pieces
        from_sq = lsb.bit_length() - 1
        pieces ^= lsb
        
        piece = board.board[from_sq]
        ptype = piece_type(piece)
        
        if ptype == PAWN:
            moves.extend(generate_pawn_moves(board, from_sq, color))
        elif ptype == KNIGHT:
            moves.extend(generate_knight_moves(board, from_sq, color))
        elif ptype == BISHOP:
            moves.extend(generate_bishop_moves(board, from_sq, color))
        elif ptype == ROOK:
            moves.extend(generate_rook_moves(board, from_sq, color))
        elif ptype == QUEEN:
            moves.extend(generate_queen_moves(board, from_sq, color))
        elif ptype == KING:
            moves.extend(generate_king_moves(board, from_sq, color))
    
    return moves

def generate_pawn_moves(board, from_sq, color):
    """Generate pawn moves"""
    moves = []
    rank = rank_of(from_sq)
    file = file_of(from_sq)
    direction = 1 if color == WHITE else -1
    start_rank = 1 if color == WHITE else 6
    
    # Forward move
    to_sq = from_sq + direction * 8
    if 0 <= to_sq < 64 and not board.board[to_sq]:
        if rank + direction == 0 or rank + direction == 7:
            for promo in [QUEEN, ROOK, BISHOP, KNIGHT]:
                moves.append((from_sq, to_sq, promo))
        else:
            moves.append((from_sq, to_sq, 0))
        
        # Double push
        if rank == start_rank:
            to_sq2 = from_sq + direction * 16
            if not board.board[to_sq2]:
                moves.append((from_sq, to_sq2, 0))
    
    # Captures
    enemy = 1 - color
    for df in [-1, 1]:
        if 0 <= file + df < 8:
            to_sq = from_sq + direction * 8 + df
            if to_sq < 64:
                if board.board[to_sq] and piece_color(board.board[to_sq]) == enemy:
                    if rank + direction == 0 or rank + direction == 7:
                        for promo in [QUEEN, ROOK, BISHOP, KNIGHT]:
                            moves.append((from_sq, to_sq, promo))
                    else:
                        moves.append((from_sq, to_sq, 0))
                if board.en_passant != -1 and to_sq == board.en_passant:
                    moves.append((from_sq, to_sq, 0))
    
    return moves

def generate_knight_moves(board, from_sq, color):
    """Generate knight moves"""
    moves = []
    rank
