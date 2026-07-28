"""
Search algorithms with all optimizations including Lazy SMP
"""

import time
import threading
from .movegen import generate_moves, filter_legal_moves, order_moves
from .evaluation import evaluate
from .transposition import TranspositionTable
from .opening import OpeningBook
from .endgame import SyzygyTablebase
from .constants import PIECE_VALUES, piece_type, ENGINE_VERSION, square_name, QUEEN, ROOK, BISHOP, KNIGHT

class Search:
    def __init__(self, board):
        self.board = board
        self.nodes = 0
        self.start_time = 0
        self.time_limit = 0
        self.best_move = None
        self.best_score = 0
        self.tt = TranspositionTable()
        self.killer_moves = [[None, None] for _ in range(100)]
        self.history = {}
        self.pv = []
        self.stop = False
        self.opening_book = OpeningBook()
        self.endgame = SyzygyTablebase()
        self.threads = 1
        self.thread_results = []
    
    def search(self, depth, time_limit=5.0):
        """Main search function with iterative deepening and Lazy SMP"""
        self.nodes = 0
        self.start_time = time.time()
        self.time_limit = time_limit
        self.best_move = None
        self.best_score = 0
        self.pv = []
        self.stop = False
        
        # Check opening book first
        fen = self.board.get_fen()
        book_move = self.opening_book.get_move(fen)
        if book_move:
            from_sq = self.parse_square(book_move[:2])
            to_sq = self.parse_square(book_move[2:4])
            promotion = 0
            if len(book_move) > 4:
                promotion = self.parse_piece_type(book_move[4])
            move = (from_sq, to_sq, promotion)
            print(f"info opening book move {book_move}")
            return move, 0
        
        # Check endgame tablebase
        tb_score = self.endgame.probe(self.board)
        if tb_score is not None:
            return None, tb_score
        
        # Clear transposition table
        self.tt.clear()
        self.killer_moves = [[None, None] for _ in range(100)]
        
        # Lazy SMP: Use multiple threads
        if self.threads > 1:
            return self.lazy_smp_search(depth, time_limit)
        
        # Single-threaded search
        return self.single_thread_search(depth, time_limit)
    
    def single_thread_search(self, depth, time_limit):
        """Single-threaded iterative deepening search"""
        # Initial aspiration window
        window = 50
        score = self.alpha_beta(1, -1000000, 1000000, 0)
        
        # Iterative deepening
        for d in range(1, depth + 1):
            if self.stop or time.time() - self.start_time > time_limit:
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
                pv_str = self.pv_to_string()
                if pv_str:
                    print(f"info pv {pv_str}")
        
        return self.best_move, score
    
    def lazy_smp_search(self, depth, time_limit):
        """Lazy SMP parallel search using multiple threads"""
        self.thread_results = []
        threads = []
        
        # Start threads with slightly different search parameters
        for i in range(self.threads):
            # Each thread gets a slightly different time limit
            thread_time = time_limit * (1.0 + (i - self.threads//2) * 0.05)
            t = threading.Thread(
                target=self.thread_search,
                args=(i, depth, thread_time)
            )
            threads.append(t)
            t.start()
        
        # Wait for first thread to finish with a result
        best_result = None
        best_score = -1000000
        
        # Wait for all threads to complete or time limit
        while time.time() - self.start_time < time_limit:
            # Check if any thread has a result
            for result in self.thread_results:
                if result and result[1] > best_score:
                    best_score = result[1]
                    best_result = result[0]
            
            # Check if all threads are done
            all_done = all(not t.is_alive() for t in threads)
            if all_done:
                break
            
            time.sleep(0.01)
        
        # Join remaining threads
        for t in threads:
            if t.is_alive():
                self.stop = True
                t.join()
        
        return best_result, best_score
    
    def thread_search(self, thread_id, depth, time_limit):
        """Thread function for Lazy SMP search"""
        # Each thread gets its own search instance
        local_board = self.board.clone()
        local_search = Search(local_board)
        local_search.tt = self.tt  # Share transposition table
        local_search.killer_moves = self.killer_moves
        local_search.history = self.history
        
        # Randomize search slightly
        if thread_id > 0:
            # Slightly different evaluation
            pass
        
        # Run search
        best_move, score = local_search.single_thread_search(depth, time_limit)
        self.thread_results.append((best_move, score))
    
    def alpha_beta(self, depth, alpha, beta, ply):
        """Alpha-beta search with all optimizations"""
        self.nodes += 1
        
        # Check time and stop flag
        if self.stop or time.time() - self.start_time > self.time_limit:
            return 0
        
        # Check for repetitions
        if self.board.halfmove_clock >= 100:
            return 0
        
        # Transposition table lookup with Zobrist
        key = self.tt.zobrist.compute_hash(self.board)
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
                return -1000000 + ply
            return 0
        
        # Null move pruning
        if depth >= 3 and not self.board.is_check(self.board.side_to_move):
            self.board.side_to_move = 1 - self.board.side_to_move
            score = -self.alpha_beta(depth - 3, -beta, -beta + 1, ply + 1)
            self.board.side_to_move = 1 - self.board.side_to_move
            if score >= beta:
                return beta
        
        # Quiescence search
        if depth == 0:
            return self.quiescence(alpha, beta, ply)
        
        # Order moves
        ordered_moves = order_moves(self.board, legal_moves, self.killer_moves, self.history, ply)
        
        # Principal variation search
        best_move = ordered_moves[0] if ordered_moves else None
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
                score = -self.alpha_beta(depth - 1, -alpha - 1, -alpha, ply + 1)
                if score > alpha and score < beta:
                    score = -self.alpha_beta(depth - 1, -beta, -alpha, ply + 1)
            
            if score > best_score:
                best_score = score
                best_move = move
                if ply == 0:
                    self.best_move = move
                    self.best_score = score
            
            # Update alpha
            if score > alpha:
                alpha = score
                if ply == 0:
                    self.pv = [move]
            
            # Beta cutoff
            if alpha >= beta:
                self.history[move] = self.history.get(move, 0) + depth * depth
                break
        
        # Store in transposition table
        flag = 'exact'
        if best_score <= alpha:
            flag = 'upper'
        elif best_score >= beta:
            flag = 'lower'
        
        if best_move:
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
    
    def pv_to_string(self):
        """Convert principal variation to string"""
        if not self.pv:
            return ""
        moves = []
        board = self.board.clone()
        for move in self.pv[:10]:  # Limit to 10 moves
            moves.append(self.move_to_string(move))
            board.make_move(move)
        return " ".join(moves)
    
    def move_to_string(self, move):
        """Convert move tuple to string"""
        from_sq, to_sq, promotion = move
        result = square_name(from_sq) + square_name(to_sq)
        if promotion:
            result += {QUEEN: 'q', ROOK: 'r', BISHOP: 'b', KNIGHT: 'n'}[promotion]
        return result
    
    def parse_square(self, sq_str):
        """Parse square from string"""
        if len(sq_str) != 2:
            return -1
        file = ord(sq_str[0]) - ord('a')
        rank = ord(sq_str[1]) - ord('1')
        if 0 <= file < 8 and 0 <= rank < 8:
            return rank * 8 + file
        return -1
    
    def parse_piece_type(self, char):
        """Parse promotion piece type"""
        return {'q': QUEEN, 'r': ROOK, 'b': BISHOP, 'n': KNIGHT}.get(char, 0)
