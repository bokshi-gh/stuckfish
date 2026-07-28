"""
Position evaluation with king safety and pawn structure
"""

from .constants import *
from .bitboard import file_of

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

KING_MIDDLE_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20, -10,-20,-20,-20,-20,-20,-20,-10,
    20,20,0,0,0,0,20,20, 20,30,10,0,0,10,30,20
]

KING_ENDGAME_TABLE = [
    0,10,20,30,30,20,10,0, 10,20,30,40,40,30,20,10,
    20,30,40,50,50,40,30,20, 30,40,50,60,60,50,40,30,
    30,40,50,60,60,50,40,30, 20,30,40,50,50,40,30,20,
    10,20,30,40,40,30,20,10, 0,10,20,30,30,20,10,0
]

def mirror_table(table, sq):
    """Mirror a piece-square table for black"""
    return table[((7 - (sq >> 3)) * 8 + (sq & 7))]

def evaluate(board):
    """Evaluate the current board position with king safety and pawn structure"""
    score = 0
    
    # Material and positional evaluation
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
            # Use different king tables based on material
            if board.piece_bitboards[QUEEN] == 0 and board.piece_bitboards[ROOK] == 0:
                val = KING_ENDGAME_TABLE[sq]
            else:
                val = KING_MIDDLE_TABLE[sq]
        else:
            val = 0
        
        if color == BLACK:
            if ptype == KING:
                if board.piece_bitboards[QUEEN] == 0 and board.piece_bitboards[ROOK] == 0:
                    val = mirror_table(KING_ENDGAME_TABLE, sq)
                else:
                    val = mirror_table(KING_MIDDLE_TABLE, sq)
            else:
                val = mirror_table(
                    PAWN_TABLE if ptype == PAWN else
                    KNIGHT_TABLE if ptype == KNIGHT else
                    BISHOP_TABLE if ptype == BISHOP else
                    ROOK_TABLE if ptype == ROOK else
                    QUEEN_TABLE if ptype == QUEEN else
                    KING_MIDDLE_TABLE, sq
                )
        
        score += val * (1 if color == WHITE else -1)
    
    # King safety (simplified)
    # Penalize exposed kings
    for color in [WHITE, BLACK]:
        king_sq = board.king_square[color]
        if king_sq != -1:
            # Count enemy pieces attacking king
            enemy = 1 - color
            attackers = 0
            # Check if king has pawn shield
            pawn_shield = 0
            for offset in [-9, -8, -7, -1, 1, 7, 8, 9]:
                sq = king_sq + offset
                if 0 <= sq < 64:
                    piece = board.board[sq]
                    if piece and piece_type(piece) == PAWN and piece_color(piece) == color:
                        pawn_shield += 1
            
            # Penalize weak king shield
            if pawn_shield < 3:
                score += (-20) * (3 - pawn_shield) * (1 if color == WHITE else -1)
    
    # Pawn structure (simplified)
    # Penalize doubled pawns
    for color in [WHITE, BLACK]:
        pawns = board.piece_bitboards[PAWN] & board.color_bitboards[color]
        file_counts = [0] * 8
        while pawns:
            sq = (pawns & -pawns).bit_length() - 1
            pawns &= pawns - 1
            file_counts[file_of(sq)] += 1
        
        for count in file_counts:
            if count > 1:
                score += (-10 * (count - 1)) * (1 if color == WHITE else -1)
    
    return score
