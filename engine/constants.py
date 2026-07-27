"""
Chess constants and piece definitions
Author: Rajesh Thapa (bokshi)
"""

# Piece types
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

# Colors
WHITE = 0
BLACK = 1

# Piece encoding: color * 8 + piece_type
def make_piece(color, piece_type):
    return color * 8 + piece_type

def piece_color(piece):
    return 0 if piece < 8 else 1

def piece_type(piece):
    return piece % 8

def piece_symbol(piece):
    if piece == 0:
        return '.'
    symbols = ['', 'P', 'N', 'B', 'R', 'Q', 'K']
    color = piece_color(piece)
    symbol = symbols[piece_type(piece)]
    return symbol.lower() if color == BLACK else symbol

# Square indices
A1, B1, C1, D1, E1, F1, G1, H1 = 0, 1, 2, 3, 4, 5, 6, 7
A2, B2, C2, D2, E2, F2, G2, H2 = 8, 9, 10, 11, 12, 13, 14, 15
A3, B3, C3, D3, E3, F3, G3, H3 = 16, 17, 18, 19, 20, 21, 22, 23
A4, B4, C4, D4, E4, F4, G4, H4 = 24, 25, 26, 27, 28, 29, 30, 31
A5, B5, C5, D5, E5, F5, G5, H5 = 32, 33, 34, 35, 36, 37, 38, 39
A6, B6, C6, D6, E6, F6, G6, H6 = 40, 41, 42, 43, 44, 45, 46, 47
A7, B7, C7, D7, E7, F7, G7, H7 = 48, 49, 50, 51, 52, 53, 54, 55
A8, B8, C8, D8, E8, F8, G8, H8 = 56, 57, 58, 59, 60, 61, 62, 63

# Square names
SQUARE_NAMES = [
    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'
]

def square_name(sq):
    return SQUARE_NAMES[sq]

def parse_square(name):
    if len(name) != 2:
        return -1
    file = ord(name[0]) - ord('a')
    rank = ord(name[1]) - ord('1')
    if 0 <= file < 8 and 0 <= rank < 8:
        return rank * 8 + file
    return -1

# Castle rights
CASTLE_WHITE_KING = 1
CASTLE_WHITE_QUEEN = 2
CASTLE_BLACK_KING = 4
CASTLE_BLACK_QUEEN = 8
CASTLE_ALL = 15

# Piece values
PIECE_VALUES = {
    PAWN: 100,
    KNIGHT: 320,
    BISHOP: 330,
    ROOK: 500,
    QUEEN: 900,
    KING: 20000
}
