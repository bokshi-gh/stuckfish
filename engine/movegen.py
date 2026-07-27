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
    rank = rank_of(from_sq)
    file = file_of(from_sq)
    
    knight_moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
    
    for dr, df in knight_moves:
        nr, nf = rank + dr, file + df
        if 0 <= nr < 8 and 0 <= nf < 8:
            to_sq = nr * 8 + nf
            piece = board.board[to_sq]
            if not piece or piece_color(piece) != color:
                moves.append((from_sq, to_sq, 0))
    
    return moves

def generate_sliding_moves(board, from_sq, color, directions):
    """Generate sliding piece moves"""
    moves = []
    rank = rank_of(from_sq)
    file = file_of(from_sq)
    occupancy = board.get_occupancy()
    
    for dr, df in directions:
        r, f = rank + dr, file + df
        while 0 <= r < 8 and 0 <= f < 8:
            to_sq = r * 8 + f
            piece = board.board[to_sq]
            if piece:
                if piece_color(piece) != color:
                    moves.append((from_sq, to_sq, 0))
                break
            moves.append((from_sq, to_sq, 0))
            r += dr
            f += df
    
    return moves

def generate_bishop_moves(board, from_sq, color):
    return generate_sliding_moves(board, from_sq, color, [(-1,-1),(-1,1),(1,-1),(1,1)])

def generate_rook_moves(board, from_sq, color):
    return generate_sliding_moves(board, from_sq, color, [(-1,0),(1,0),(0,-1),(0,1)])

def generate_queen_moves(board, from_sq, color):
    return generate_sliding_moves(board, from_sq, color, 
        [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)])

def generate_king_moves(board, from_sq, color):
    """Generate king moves including castling"""
    moves = []
    rank = rank_of(from_sq)
    file = file_of(from_sq)
    
    king_moves = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    
    for dr, df in king_moves:
        nr, nf = rank + dr, file + df
        if 0 <= nr < 8 and 0 <= nf < 8:
            to_sq = nr * 8 + nf
            piece = board.board[to_sq]
            if not piece or piece_color(piece) != color:
                moves.append((from_sq, to_sq, 0))
    
    # Castling
    if color == WHITE:
        if from_sq == E1:
            # King side
            if (board.castle_rights & CASTLE_WHITE_KING and 
                not board.board[F1] and not board.board[G1] and
                not board.is_square_attacked(E1, BLACK) and
                not board.is_square_attacked(F1, BLACK)):
                moves.append((E1, G1, 0))
            # Queen side
            if (board.castle_rights & CASTLE_WHITE_QUEEN and
                not board.board[D1] and not board.board[C1] and not board.board[B1] and
                not board.is_square_attacked(E1, BLACK) and
                not board.is_square_attacked(D1, BLACK)):
                moves.append((E1, C1, 0))
    else:
        if from_sq == E8:
            # King side
            if (board.castle_rights & CASTLE_BLACK_KING and
                not board.board[F8] and not board.board[G8] and
                not board.is_square_attacked(E8, WHITE) and
                not board.is_square_attacked(F8, WHITE)):
                moves.append((E8, G8, 0))
            # Queen side
            if (board.castle_rights & CASTLE_BLACK_QUEEN and
                not board.board[D8] and not board.board[C8] and not board.board[B8] and
                not board.is_square_attacked(E8, WHITE) and
                not board.is_square_attacked(D8, WHITE)):
                moves.append((E8, C8, 0))
    
    return moves

def filter_legal_moves(board, moves):
    """Filter moves to only legal moves"""
    legal_moves = []
    for move in moves:
        board_clone = board.clone()
        board_clone.make_move(move)
        if not board_clone.is_check(board.side_to_move):
            legal_moves.append(move)
    return legal_moves

def order_moves(board, moves, killer_moves, history, ply):
    """Order moves for better pruning"""
    scored = []
    
    for move in moves:
        score = 0
        from_sq, to_sq, promo = move
        
        # MVV-LVA for captures
        victim = board.board[to_sq]
        if victim:
            victim_val = PIECE_VALUES[piece_type(victim)]
            attacker = board.board[from_sq]
            attacker_val = PIECE_VALUES[piece_type(attacker)]
            score = 10 * victim_val - attacker_val
        
        # Promotions
        if promo:
            score += PIECE_VALUES[promo] + 500
        
        # Killer moves
        if killer_moves and ply < len(killer_moves):
            if move == killer_moves[ply][0]:
                score += 1000
            elif move == killer_moves[ply][1]:
                score += 900
        
        # History heuristic
        score += history.get(move, 0)
        
        scored.append((score, move))
    
    scored.sort(reverse=True)
    return [move for _, move in scored]
