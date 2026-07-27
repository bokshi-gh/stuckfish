"""
Perft testing for move generation validation
Author: Rajesh Thapa (bokshi)
"""

import time
from .movegen import generate_moves, filter_legal_moves

class Perft:
    def __init__(self, board):
        self.board = board
        self.nodes = 0
        self.captures = 0
        self.en_passant = 0
        self.castles = 0
        self.promotions = 0
        self.checks = 0
        self.checkmates = 0
    
    def perft(self, depth):
        """Run perft test to given depth"""
        if depth == 0:
            return 1
        
        moves = generate_moves(self.board)
        legal_moves = filter_legal_moves(self.board, moves)
        
        if depth == 1:
            return len(legal_moves)
        
        total = 0
        for move in legal_moves:
            board_copy = self.board.clone()
            board_copy.make_move(move)
            
            # Track move types
            from_sq, to_sq, promo = move
            if board_copy.board[to_sq]:
                self.captures += 1
            if promo:
                self.promotions += 1
            if self.board.en_passant != -1 and to_sq == self.board.en_passant:
                self.en_passant += 1
            
            # Check for castling
            piece = self.board.board[from_sq]
            if piece_type(piece) == KING and abs(to_sq - from_sq) == 2:
                self.castles += 1
            
            # Check for check/checkmate
            if board_copy.is_check(1 - self.board.side_to_move):
                self.checks += 1
                # Check if checkmate
                next_moves = generate_moves(board_copy)
                next_legal = filter_legal_moves(board_copy, next_moves)
                if not next_legal:
                    self.checkmates += 1
            
            total += self.perft_recursive(board_copy, depth - 1)
        
        return total
    
    def perft_recursive(self, board, depth):
        """Recursive perft calculation"""
        if depth == 0:
            return 1
        
        moves = generate_moves(board)
        legal_moves = filter_legal_moves(board, moves)
        
        if depth == 1:
            return len(legal_moves)
        
        total = 0
        for move in legal_moves:
            board_copy = board.clone()
            board_copy.make_move(move)
            total += self.perft_recursive(board_copy, depth - 1)
        
        return total
    
    def perft_divide(self, depth):
        """Perft divide - show move counts for each first move"""
        moves = generate_moves(self.board)
        legal_moves = filter_legal_moves(self.board, moves)
        
        results = []
        total = 0
        
        for move in legal_moves:
            board_copy = self.board.clone()
            board_copy.make_move(move)
            count = self.perft_recursive(board_copy, depth - 1)
            results.append((move, count))
            total += count
        
        return results, total
    
    def run_perft(self, depth, show_progress=True):
        """Run complete perft test with statistics"""
        print(f"\n=== Perft Test Depth {depth} ===")
        start_time = time.time()
        
        results, total = self.perft_divide(depth)
        
        elapsed = time.time() - start_time
        
        # Print results
        print(f"\nMove counts at depth {depth}:")
        for move, count in results:
            move_str = f"{square_name(move[0])}{square_name(move[1])}"
            if move[2]:
                move_str += {QUEEN: 'q', ROOK: 'r', BISHOP: 'b', KNIGHT: 'n'}[move[2]]
            print(f"  {move_str}: {count}")
        
        print(f"\nTotal: {total}")
        print(f"Time: {elapsed:.3f} seconds")
        print(f"Nodes/sec: {total / elapsed:.0f}")
        
        return total
    
    def perft_suite(self):
        """Run a series of perft tests"""
        test_positions = [
            ("Starting position", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
            ("Position 2", "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"),
            ("Position 3", "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"),
            ("Position 4", "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"),
            ("Position 5", "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"),
        ]
        
        results = []
        for name, fen in test_positions:
            self.board.set_fen(fen)
            print(f"\nTesting: {name}")
            print(f"FEN: {fen}")
            
            for depth in range(1, 5):
                self.reset_counters()
                count = self.perft(depth)
                print(f"  Depth {depth}: {count} nodes")
            
            results.append((name, self.nodes))
        
        return results
    
    def reset_counters(self):
        """Reset all counters"""
        self.nodes = 0
        self.captures = 0
        self.en_passant = 0
        self.castles = 0
        self.promotions = 0
        self.checks = 0
        self.checkmates = 0

# Import needed constants
from .constants import square_name, QUEEN, ROOK, BISHOP, KNIGHT, piece_type
