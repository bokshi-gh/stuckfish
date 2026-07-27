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
            
            elif command == "
