"""
UCI (Universal Chess Interface) protocol implementation
"""

import sys
import time
import functools
from .board import Board
from .search import Search
from .transposition import TranspositionTable
from .constants import (
    square_name, QUEEN, ROOK, BISHOP, KNIGHT,
    ENGINE_NAME, ENGINE_VERSION, ENGINE_AUTHOR, UCI_OPTIONS
)

# Force all prints to flush immediately for UCI protocol communication
print = functools.partial(print, flush=True)

class UCI:
    def __init__(self):
        self.board = Board()
        self.search = Search(self.board)
        self.is_running = True
        self.hash_size = UCI_OPTIONS["Hash"]["default"]
        self.threads = UCI_OPTIONS["Threads"]["default"]
        self.ponder = UCI_OPTIONS["Ponder"]["default"]
        self.own_book = UCI_OPTIONS["OwnBook"]["default"]
    
    def run(self):
        """Main UCI loop"""
        print(f"id name {ENGINE_NAME} {ENGINE_VERSION}")
        print(f"id author {ENGINE_AUTHOR}")
        
        # Print UCI options
        for name, options in UCI_OPTIONS.items():
            if options["type"] == "spin":
                print(f"option name {name} type {options['type']} default {options['default']} min {options['min']} max {options['max']}")
            elif options["type"] == "check":
                print(f"option name {name} type {options['type']} default {'true' if options['default'] else 'false'}")
        
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
                print(f"id name {ENGINE_NAME} {ENGINE_VERSION}")
                print(f"id author {ENGINE_AUTHOR}")
                print("uciok")
            
            elif command == "isready":
                print("readyok")
            
            elif command == "ucinewgame":
                self.board = Board()
                self.search = Search(self.board)
                self.search.threads = self.threads
                self.search.tt = TranspositionTable(self.hash_size)
            
            elif command == "setoption":
                self.handle_setoption(parts[1:])
            
            elif command == "position":
                self.handle_position(parts[1:])
            
            elif command == "go":
                self.handle_go(parts[1:])
            
            elif command == "stop":
                self.search.stop = True
            
            elif command == "d":
                print(self.board)
    
    def handle_setoption(self, args):
        """Handle 'setoption' command"""
        if len(args) < 4:
            return
        
        option_name = args[1]
        if args[2] == "value":
            option_value = args[3]
            
            if option_name == "Hash":
                try:
                    self.hash_size = int(option_value)
                    self.search.tt = TranspositionTable(self.hash_size)
                except ValueError:
                    pass
            elif option_name == "Threads":
                try:
                    self.threads = int(option_value)
                    self.search.threads = self.threads
                except ValueError:
                    pass
            elif option_name == "Ponder":
                self.ponder = option_value.lower() in ["true", "1", "yes", "on"]
            elif option_name == "OwnBook":
                self.own_book = option_value.lower() in ["true", "1", "yes", "on"]
                self.search.own_book = self.own_book
    
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
        infinite = False
        
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
            elif args[i] == "infinite":
                infinite = True
        
        # Time limit
        if infinite:
            time_limit = 300
        elif movetime > 0:
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
        
        # Reset stop flag
        self.search.stop = False
        
        start_time = time.time()
        best_move, score = self.search.search(depth, time_limit)
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
