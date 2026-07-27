"""
Search algorithms for chess engine
Author: Rajesh Thapa (bokshi)
"""

import time
from .movegen import generate_moves, filter_legal_moves
from .evaluation import evaluate

class Search:
    def __init__(self, board):
        self.board = board
        self.nodes = 0
        self.start_time = 0
        self.time_limit = 0
        self.best_move = None
    
    def search(self, depth, time_limit=5.0):
        """Main search function"""
        self.nodes = 0
        self.start_time = time.time()
        self.time_limit = time_limit
        self.best_move = None
        
        # Iterative deepening
        for d in range(1, depth + 1):
            if time.time() - self.start_time > time_limit:
                break
            
            score = self.alpha_beta(d, -1000000, 1000000, 0)
            if self.best_move:
                print(f"info depth {d} score {score} nodes {self.nodes}")
        
        return self.best_move, self.best_move
    
    def alpha_beta(self, depth, alpha, beta, ply):
        """Alpha-beta minimax search"""
        self.nodes += 1
        
        # Check time
        if time.time() - self.start_time > self.time_limit:
            return 0
        
        # Generate moves
        moves = generate_moves(self.board)
        legal_moves = filter_legal_moves(self.board, moves)
        
        # Terminal positions
        if not legal_moves:
            if self.board.is_check(self.board.side_to_move):
                return -1000000 + ply
            return 0
        
        # Depth reached
        if depth == 0:
            return evaluate(self.board) * (1 if self.board.side_to_move == 0 else -1)
        
        # Search
        best_move = legal_moves[0]
        for move in legal_moves:
            board_copy = self.board.clone()
            board_copy.make_move(move)
            
            score = -self.alpha_beta(depth - 1, -beta, -alpha, ply + 1)
            
            if score > alpha:
                alpha = score
                best_move = move
                if ply == 0:
                    self.best_move = move
            
            if alpha >= beta:
                break
        
        return alpha
