"""
UCI (Universal Chess Interface) protocol implementation
Author: Rajesh Thapa (bokshi)
"""

import sys
import time
from .board import Board
from .search import Search
from .constants import square_name, QUEEN, ROOK, BISHOP, KNIGHT

class UCI:
    def __init__(self):
        self.board = Board()
        self.search = Search(self.board)
        self.is_running = True
    
    def run(self):
        """Main UCI loop"""
        print("id name Stuckfish")
        print("id author Rajesh Thapa (bokshi)")
        print("option name Hash type spin default 64 min 1 max 1024")
        print("option name Ponder type check default false")
        print("uciok")
        
        while self.is_running:
            line = sys.stdin.readline().strip()
            if not line:
                continue
            
            parts = line.split()
            command = parts[0]
            
            if command == "quit":
                self.is_running = False
            
            elif command == "uci":
                print("id name Stuckfish")
                print("id author Rajesh Thapa (bokshi)")
                print("uciok")
            
            elif command == "isready":
                print("readyok")
            
            elif command == "ucinewgame":
                self.board = Board()
                self.search = Search(self.board)
            
            elif command == "position":
                self.handle_position(parts[1:])
            
            elif command == "go":
                self.handle_go(parts[1:])
            
            elif command == "d":
                print(self.board)
            
            elif command == "stop":
                pass
    
    def handle_position(self, args):
        """Handle 'position' command"""
        if args[0] == "fen":
            fen = " ".join(args[1:7])
            self.board.set_fen(fen)
            remaining = args[7:]
        else:  # "startpos"
            self.board.reset()
            remaining = args[1:]
        
        if remaining and remaining[0] == "moves":
            for move_str in remaining[1:]:
                from_sq = self.parse_square(move_str[:2])
                to_sq = self.parse_square(move_str[2:4])
                promotion = 0
                if len(move_str) > 4:
                    promotion = self.parse_piece_type(move_str[4])
                self.board.make_move((from_sq, to_sq, promotion))
    
    def handle_go(self, args):
        """Handle 'go' command"""
        depth = 4
        movetime = 0
        wtime = btime = winc = binc = 0
        
        for i in range(0, len(args), 2):
            if i + 1 >= len(args):
                break
            if args[i] == "depth":
                depth = int(args[i + 1])
            elif args[i] == "wtime":
                wtime = int(args[i + 1])
            elif args[i] == "btime":
                btime = int(args[i + 1])
            elif args[i] == "winc":
                winc = int(args[i + 1])
            elif args[i] == "binc":
                binc = int(args[i + 1])
            elif args[i] == "movetime":
                movetime = int(args[i + 1])
        
        # Time limit
        if movetime > 0:
            time_limit = movetime / 1000
        else:
            time_limit = 5.0
            if self.board.side_to_move == 0:
                if wtime > 0:
                    time_limit = wtime / 1000 / 40
                    if winc > 0:
                        time_limit += winc / 1000
            else:
                if btime > 0:
                    time_limit = btime / 1000 / 40
                    if binc > 0:
                        time_limit += binc / 1000
        
        depth = min(depth, 20)
        time_limit = max(0.1, min(time_limit, 300))
        
        start_time = time.time()
        best_move, _ = self.search.search(depth, time_limit)
        elapsed = time.time() - start_time
        
        if best_move:
            print(f"bestmove {self.move_to_string(best_move)}")
        else:
            print("bestmove (none)")
    
    def parse_square(self, sq_str):
        if len(sq_str) != 2:
            return -1
        file = ord(sq_str[0]) - ord('a')
        rank = ord(sq_str[1]) - ord('1')
        if 0 <= file < 8 and 0 <= rank < 8:
            return rank * 8 + file
        return -1
    
    def parse_piece_type(self, char):
        return {'q': QUEEN, 'r': ROOK, 'b': BISHOP, 'n': KNIGHT}.get(char, 0)
    
    def move_to_string(self, move):
        from_sq, to_sq, promotion = move
        result = square_name(from_sq) + square_name(to_sq)
        if promotion:
            result += {QUEEN: 'q', ROOK: 'r', BISHOP: 'b', KNIGHT: 'n'}[promotion]
        return result
