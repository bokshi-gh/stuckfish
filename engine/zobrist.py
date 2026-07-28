"""
Zobrist hashing for transposition table
"""

import random

class Zobrist:
    def __init__(self):
        self.piece_keys = [[[0] * 64 for _ in range(7)] for _ in range(2)]
        self.castle_keys = [0] * 16
        self.ep_keys = [0] * 64
        self.side_key = 0
        
        # Initialize random keys
        random.seed(42)  # Fixed seed for reproducibility
        for color in range(2):
            for piece in range(7):
                for sq in range(64):
                    self.piece_keys[color][piece][sq] = random.getrandbits(64)
        for i in range(16):
            self.castle_keys[i] = random.getrandbits(64)
        for sq in range(64):
            self.ep_keys[sq] = random.getrandbits(64)
        self.side_key = random.getrandbits(64)
    
    def compute_hash(self, board):
        """Compute Zobrist hash for current board position"""
        hash_key = 0
        
        # Piece positions
        for sq in range(64):
            piece = board.board[sq]
            if piece:
                color = piece_color(piece)
                ptype = piece_type(piece)
                hash_key ^= self.piece_keys[color][ptype][sq]
        
        # Castle rights
        hash_key ^= self.castle_keys[board.castle_rights]
        
        # En passant
        if board.en_passant != -1:
            hash_key ^= self.ep_keys[board.en_passant]
        
        # Side to move
        if board.side_to_move == BLACK:
            hash_key ^= self.side_key
        
        return hash_key

# Import needed constants
from .constants import piece_color, piece_type
