"""
Position evaluation functions
Author: Rajesh Thapa (bokshi)
"""

from .constants import *

# Piece-square tables
PAWN_TABLE = [
    0,0,0,0,0,0,0,0, 50,50,50,50,50,50,50,50,
    10,10,20,30,30,20,10,10, 5,5,10,25,25,10,5,5,
    0,0,0,20,20,0,0,0, 5,-5,-10,0,0,-10,-5,5,
    5,10,10,-20,-20,10,10,5, 0,0,0,0,0,0,0,0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50, -40,-20,0,0,0,0,-20,-40,
    -30,0,10,15,15,10,0,-30, -30,5,15,20,20,15,5,-30,
    -30,0,15,20,20,15,0,-30, -30,5,10,15,15,10,5,-30,
    -40,-20,0,5,5,0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20, -10,0,0,0,0,0,0,-10,
    -10,0,5,10,10,5,0,-10, -10,5,5,10,10,5,5,-10,
    -10,0,10,10,10,10,0,-10, -10,10,10,10,10,10,10,-10,
    -10,5,0,0,0,0,5,-10, -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
    0,0,0,0,0,0,0,0, 5,10,10,10,10,10,10,5,
    -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5,
    -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5,
    -5,0,0,0,0,0,0,-5, 0,0,0,5,5,0,0,0
]

QUEEN_TABLE = [
    -20,-10,-10,-5,-5,-10,-10,-20, -10,0,0,0,0,0,0,-10,
    -10,0,5,5,5,5,0,-10, -5,0,5,5,5,5,0,-5,
    0,0,5,5,5,5,0,-5, -10,5,5,5,5,5,0,-10,
    -10,0,5,0,0,0,0,-10, -20,-10,-10,-5,-5,-10,-10,-20
]

KING_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20, -10,-20,-20,-20,-20,-20,-20,-10,
    20,20,0,0,0,0,20,20, 20,30,10,0,0,10,30,20
]

def mirror_table(table, sq):
    """Mirror a piece-square table for black"""
    return table[((7 - (sq >> 3)) * 8 + (sq & 7))]

def evaluate(board):
    """Evaluate the current board position"""
    score = 0
    
    for sq in range(64):
        piece = board.board[sq]
        if not piece:
            continue
        
        color = piece_color(piece)
        ptype = piece_type(piece)
        
        # Material
        score += PIECE_VALUES[ptype] * (1 if color == WHITE else -1)
        
        # Positional
        if ptype == PAWN:
            val = PAWN_TABLE[sq]
        elif ptype == KNIGHT:
            val = KNIGHT_TABLE[sq]
        elif ptype == BISHOP:
            val = BISHOP_TABLE[sq]
        elif ptype == ROOK:
            val = ROOK_TABLE[sq]
        elif ptype == QUEEN:
            val = QUEEN_TABLE[sq]
        elif ptype == KING:
            val = KING_TABLE[sq]
        else:
            val = 0
        
        if color == BLACK:
            val = mirror_table(PAWN_TABLE if ptype == PAWN else
                             KNIGHT_TABLE if ptype == KNIGHT else
                             BISHOP_TABLE if ptype == BISHOP else
                             ROOK_TABLE if ptype == ROOK else
                             QUEEN_TABLE if ptype == QUEEN else
                             KING_TABLE, sq)
        
        score += val * (1 if color == WHITE else -1)
    
    return score
