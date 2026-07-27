"""
Search algorithms with all optimizations
Author: Rajesh Thapa (bokshi)
"""

import time
from .movegen import generate_moves, filter_legal_moves, order_moves
from .evaluation import evaluate
from .transposition import TranspositionTable
from .constants import PIECE_VALUES, piece_type

class Search:
    def __init__(self, board):
        self.board = board
        self.nodes = 0
        self.start_time = 0
        self.time_limit = 0
        self.best_move = None
        self.tt = TranspositionTable()
        self.killer_moves = [[None, None] for _ in range(100)]
        self.history = {}
        self.pv = []  # Principal variation
    
    def search(self, depth, time_limit=5.0):
        """Main search function with iterative deepening"""
        self.nodes = 0
        self.start_time = time.time()
        self.time_limit = time_limit
        self.best_move = None
        self.pv = []
        self.tt.clear()
        self.killer_moves = [[None, None] for _ in range(100)]
        
        # Initial aspiration window
        window = 50
        score = self.alpha_beta(1, -1000000, 1000000, 0)
        
        # Iterative deepening
        for d in range(1, depth + 1):
            if time.time() - self.start_time > self.time_limit:
                break
            
            # Aspiration windows
            alpha = score - window
            beta = score + window
            
            if d >= 3:
                score = self.alpha_beta(d, alpha, beta, 0)
                # If outside window, research with full window
                if score <= alpha or score >= beta:
                    score = self.alpha_beta(d, -1000000, 1000000, 0)
            else:
                score = self.alpha_beta(d, -1000000, 1000000, 0)
            
            # Update window for next iteration
            window = 50
            
            # Print info
            elapsed = time.time() - self.start_time
            print(f"info depth {d} score {score} nodes {self.nodes} time {int(elapsed*1000)}")
            
            if self.best_move:
                print(f"info pv {' '.join([self.move_to_string(self.best_move)])}")
        
        return self.best_move, score
    
    def alpha_beta(self, depth, alpha, beta, ply):
        """Alpha-beta search with all optimizations"""
        self.nodes += 1
        
        # Check time
        if time.time() - self.start_time > self.time_limit:
            return 0
        
        # Check for repetitions (simplified)
        if self.board.halfmove_clock >= 100:
            return 0
        
        # Transposition table lookup
        key = self.get_zobrist_key()
        tt_entry = self.tt.lookup(key, depth, alpha, beta, ply)
        if tt_entry:
            best_move, score = tt_entry
            if depth >= 0:
                return score
        
        # Generate moves
        moves = generate_moves(self.board)
        legal_moves = filter_legal_moves(self.board, moves)
        
        # Check for terminal positions
        if not legal_moves:
            if self.board.is_check(self.board.side_to_move):
                return -1000000 + ply  # Checkmate
            return 0  # Stalemate
        
        # Null move pruning
        if depth >= 3 and not self.board.is_check(self.board.side_to_move):
            self.board.side_to_move = 1 - self.board.side_to_move
            score = -self.alpha_beta(depth - 3, -beta, -beta + 1, ply + 1)
            self.board.side_to_move = 1 - self.board.side_to_move
            if score >= beta:
                return beta
        
        # Check if depth is 0 (quiescence)
        if depth == 0:
            return self.quiescence(alpha, beta, ply)
        
        # Order moves
        ordered_moves = order_moves(self.board, legal_moves, self.killer_moves, self.history, ply)
        
        # Principal variation search
        best_move = ordered_moves[0]
        best_score = -1000000
        
        for i, move in enumerate(ordered_moves):
            # Make move
            board_copy = self.board.clone()
            board_copy.make_move(move)
            
            # Store killer moves
            if i >= 2:
                self.killer_moves[ply][i % 2] = move
            
            # PVS
            if i == 0:
                score = -self.alpha_beta(depth - 1, -beta, -alpha, ply + 1)
            else:
                # Zero window search
                score = -self.alpha_beta(depth - 1, -alpha - 1, -alpha, ply + 1)
                if score > alpha and score < beta:
                    # Re-search with full window
                    score = -self.alpha_beta(depth - 1, -beta, -alpha, ply + 1)
            
            if score > best_score:
                best_score = score
                best_move = move
                if ply == 0:
                    self.best_move = move
            
            # Update alpha
            if score > alpha:
                alpha = score
                # Store PV
                if ply == 0:
                    self.pv = [move]
            
            # Beta cutoff
            if alpha >= beta:
                # Store in history
                self.history[move] = self.history.get(move, 0) + depth * depth
                break
        
        # Store in transposition table
        flag = 'exact'
        if best_score <= alpha:
            flag = 'upper'
        elif best_score >= beta:
            flag = 'lower'
        
        self.tt.store(key, depth, best_score, flag, best_move, ply)
        
        return best_score
    
    def quiescence(self, alpha, beta, ply):
        """Quiescence search to avoid horizon effect"""
        self.nodes += 1
        
        # Evaluate position
        score = evaluate(self.board)
        
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
        
        # Generate capture moves
        moves = generate_moves(self.board)
        legal_moves = filter_legal_moves(self.board, moves)
        
        # Filter to only captures and promotions
        capture_moves = []
        for move in legal_moves:
            from_sq, to_sq, promo = move
            if promo or self.board.board[to_sq]:
                capture_moves.append(move)
        
        # Order capture moves (MVV-LVA)
        scored_moves = []
        for move in capture_moves:
            from_sq, to_sq, promo = move
            victim = self.board.board[to_sq]
            if victim:
                victim_val = PIECE_VALUES[piece_type(victim)]
                attacker = self.board.board[from_sq]
                attacker_val = PIECE_VALUES[piece_type(attacker)]
                score = 10 * victim_val - attacker_val
            else:
                score = PIECE_VALUES[promo] if promo else 0
            scored_moves.append((score, move))
        
        scored_moves.sort(reverse=True)
        capture_moves = [move for _, move in scored_moves]
        
        for move in capture_moves:
            board_copy = self.board.clone()
            board_copy.make_move(move)
            
            score = -self.quiescence(-beta, -alpha, ply + 1)
            
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        
        return alpha
    
    def get_zobrist_key(self):
        """Get Zobrist hash key (simplified)"""
        # This is a placeholder - implement proper Zobrist hashing
        return hash(self.board.get_fen())
    
    def move_to_string(self, move):
        """Convert move tuple to string"""
        from_sq, to_sq, promotion = move
        result = square_name(from_sq) + square_name(to_sq)
        if promotion:
            result += {QUEEN: 'q', ROOK: 'r', BISHOP: 'b', KNIGHT: 'n'}[promotion]
        return result

# Import needed constants
from .constants import square_name, QUEEN, ROOK, BISHOP, KNIGHT
