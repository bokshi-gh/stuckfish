"""
Chess board representation
Author: Rajesh Thapa (bokshi)
"""

from .constants import *
from .bitboard import *

class Board:
    def __init__(self, fen=None):
        self.board = [0] * 64
        self.color_bitboards = [0, 0]
        self.piece_bitboards = [0] * 7
        self.side_to_move = WHITE
        self.castle_rights = CASTLE_ALL
        self.en_passant = -1
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.hash = 0
        
        if fen:
            self.set_fen(fen)
        else:
            self.reset()
    
    def reset(self):
        """Reset board to starting position"""
        self.board = [0] * 64
        self.color_bitboards = [0, 0]
        self.piece_bitboards = [0] * 7
        
        # White pieces
        self._set_piece(A1, make_piece(WHITE, ROOK))
        self._set_piece(B1, make_piece(WHITE, KNIGHT))
        self._set_piece(C1, make_piece(WHITE, BISHOP))
        self._set_piece(D1, make_piece(WHITE, QUEEN))
        self._set_piece(E1, make_piece(WHITE, KING))
        self._set_piece(F1, make_piece(WHITE, BISHOP))
        self._set_piece(G1, make_piece(WHITE, KNIGHT))
        self._set_piece(H1, make_piece(WHITE, ROOK))
        for i in range(8):
            self._set_piece(A2 + i, make_piece(WHITE, PAWN))
        
        # Black pieces
        self._set_piece(A8, make_piece(BLACK, ROOK))
        self._set_piece(B8, make_piece(BLACK, KNIGHT))
        self._set_piece(C8, make_piece(BLACK, BISHOP))
        self._set_piece(D8, make_piece(BLACK, QUEEN))
        self._set_piece(E8, make_piece(BLACK, KING))
        self._set_piece(F8, make_piece(BLACK, BISHOP))
        self._set_piece(G8, make_piece(BLACK, KNIGHT))
        self._set_piece(H8, make_piece(BLACK, ROOK))
        for i in range(8):
            self._set_piece(A7 + i, make_piece(BLACK, PAWN))
        
        self.side_to_move = WHITE
        self.castle_rights = CASTLE_ALL
        self.en_passant = -1
        self.halfmove_clock = 0
        self.fullmove_number = 1
    
    def _set_piece(self, sq, piece):
        """Set a piece on the board"""
        if self.board[sq]:
            self._clear_piece(sq)
        if piece:
            self.board[sq] = piece
            color = piece_color(piece)
            ptype = piece_type(piece)
            bit = 1 << sq
            self.color_bitboards[color] |= bit
            self.piece_bitboards[ptype] |= bit
    
    def _clear_piece(self, sq):
        """Clear a piece from the board"""
        piece = self.board[sq]
        if piece:
            color = piece_color(piece)
            ptype = piece_type(piece)
            bit = 1 << sq
            self.color_bitboards[color] &= ~bit
            self.piece_bitboards[ptype] &= ~bit
            self.board[sq] = 0
    
    def get_piece(self, sq):
        return self.board[sq]
    
    def get_occupancy(self):
        """Get bitboard of all occupied squares"""
        return self.color_bitboards[WHITE] | self.color_bitboards[BLACK]
    
    def make_move(self, move):
        """Make a move on the board"""
        from_sq, to_sq, promotion = move
        piece = self.board[from_sq]
        
        if not piece:
            return False
        
        # Remove piece from current square
        self._clear_piece(from_sq)
        
        # Handle en passant capture
        if self.en_passant != -1 and to_sq == self.en_passant:
            captured_sq = to_sq - 8 if self.side_to_move == WHITE else to_sq + 8
            self._clear_piece(captured_sq)
        
        # Handle promotion
        if promotion:
            self._set_piece(to_sq, make_piece(self.side_to_move, promotion))
        else:
            self._set_piece(to_sq, piece)
        
        # Handle castling
        if piece_type(piece) == KING:
            if from_sq == E1 and to_sq == G1:
                self._set_piece(F1, make_piece(WHITE, ROOK))
                self._clear_piece(H1)
            elif from_sq == E1 and to_sq == C1:
                self._set_piece(D1, make_piece(WHITE, ROOK))
                self._clear_piece(A1)
            elif from_sq == E8 and to_sq == G8:
                self._set_piece(F8, make_piece(BLACK, ROOK))
                self._clear_piece(H8)
            elif from_sq == E8 and to_sq == C8:
                self._set_piece(D8, make_piece(BLACK, ROOK))
                self._clear_piece(A8)
        
        # Switch side to move
        self.side_to_move = 1 - self.side_to_move
        
        # Reset en passant
        self.en_passant = -1
        
        # Update fullmove number
        if self.side_to_move == WHITE:
            self.fullmove_number += 1
        
        return True
    
    def set_fen(self, fen):
        """Set board position from FEN string"""
        parts = fen.split()
        if len(parts) < 1:
            return
        
        # Reset board
        self.board = [0] * 64
        self.color_bitboards = [0, 0]
        self.piece_bitboards = [0] * 7
        
        # Parse piece placement
        ranks = parts[0].split('/')
        for rank_idx, rank_str in enumerate(ranks):
            rank = 7 - rank_idx
            file_idx = 0
            for char in rank_str:
                if char.isdigit():
                    file_idx += int(char)
                else:
                    sq = rank * 8 + file_idx
                    color = BLACK if char.islower() else WHITE
                    ptype = {
                        'p': PAWN, 'n': KNIGHT, 'b': BISHOP,
                        'r': ROOK, 'q': QUEEN, 'k': KING
                    }[char.lower()]
                    self._set_piece(sq, make_piece(color, ptype))
                    file_idx += 1
        
        # Parse side to move
        if len(parts) > 1:
            self.side_to_move = 0 if parts[1] == 'w' else 1
        
        # Parse castling rights
        if len(parts) > 2:
            self.castle_rights = 0
            if 'K' in parts[2]: self.castle_rights |= CASTLE_WHITE_KING
            if 'Q' in parts[2]: self.castle_rights |= CASTLE_WHITE_QUEEN
            if 'k' in parts[2]: self.castle_rights |= CASTLE_BLACK_KING
            if 'q' in parts[2]: self.castle_rights |= CASTLE_BLACK_QUEEN
        
        # Parse en passant
        if len(parts) > 3 and parts[3] != '-':
            self.en_passant = parse_square(parts[3])
        else:
            self.en_passant = -1
        
        # Parse halfmove clock
        if len(parts) > 4:
            self.halfmove_clock = int(parts[4])
        
        # Parse fullmove number
        if len(parts) > 5:
            self.fullmove_number = int(parts[5])
    
    def get_fen(self):
        """Get FEN string representation"""
        fen = []
        
        # Piece placement
        for rank in range(7, -1, -1):
            empty = 0
            for file in range(8):
                sq = rank * 8 + file
                piece = self.board[sq]
                if piece:
                    if empty:
                        fen.append(str(empty))
                        empty = 0
                    fen.append(piece_symbol(piece))
                else:
                    empty += 1
            if empty:
                fen.append(str(empty))
            if rank > 0:
                fen.append('/')
        
        fen.append(' ')
        fen.append('w' if self.side_to_move == WHITE else 'b')
        fen.append(' ')
        
        # Castling rights
        castle = ''
        if self.castle_rights & CASTLE_WHITE_KING: castle += 'K'
        if self.castle_rights & CASTLE_WHITE_QUEEN: castle += 'Q'
        if self.castle_rights & CASTLE_BLACK_KING: castle += 'k'
        if self.castle_rights & CASTLE_BLACK_QUEEN: castle += 'q'
        fen.append(castle if castle else '-')
        fen.append(' ')
        
        # En passant
        if self.en_passant != -1:
            fen.append(square_name(self.en_passant))
        else:
            fen.append('-')
        fen.append(' ')
        
        fen.append(str(self.halfmove_clock))
        fen.append(' ')
        fen.append(str(self.fullmove_number))
        
        return ''.join(fen)
    
    def __str__(self):
        """Pretty print the board"""
        result = []
        result.append("  +-----------------+\n")
        for rank in range(7, -1, -1):
            result.append(f'{rank+1} |')
            for file in range(8):
                sq = rank * 8 + file
                piece = self.board[sq]
                result.append(f' {piece_symbol(piece)}')
            result.append(' |\n')
        result.append("  +-----------------+\n")
        result.append("    a b c d e f g h\n")
        return ''.join(result)
    
    def is_check(self, color):
        """Check if the given color is in check"""
        # Find king
        king_bb = self.piece_bitboards[KING] & self.color_bitboards[color]
        if not king_bb:
            return False
        king_sq = bit_scan_forward(king_bb)
        # Simplified - would need full attack detection
        return False
    
    def is_square_attacked(self, sq, by_color):
        """Check if a square is attacked by the given color"""
        # Simplified version
        return False
    
    def clone(self):
        """Create a deep copy of the board"""
        import copy
        return copy.deepcopy(self)
