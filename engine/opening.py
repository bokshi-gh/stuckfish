"""
Opening book support
"""

import json
import random
import os

class OpeningBook:
    def __init__(self, book_file=None):
        self.book = {}
        self.load_book(book_file)
    
    def load_book(self, book_file=None):
        """Load opening book from file"""
        if book_file and os.path.exists(book_file):
            try:
                with open(book_file, 'r') as f:
                    self.book = json.load(f)
            except:
                self.book = {}
        else:
            # Default opening book (minimal)
            self.book = {
                "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": {
                    "e2e4": 100,
                    "d2d4": 90,
                    "g1f3": 80,
                    "c2c4": 70
                }
            }
    
    def get_move(self, fen):
        """Get a move from the opening book"""
        if fen in self.book:
            moves = self.book[fen]
            if moves:
                # Weighted random selection
                total = sum(moves.values())
                if total > 0:
                    rand = random.randint(0, total - 1)
                    for move, weight in moves.items():
                        rand -= weight
                        if rand < 0:
                            return move
        return None
    
    def add_move(self, fen, move, weight=1):
        """Add a move to the opening book"""
        if fen not in self.book:
            self.book[fen] = {}
        self.book[fen][move] = self.book[fen].get(move, 0) + weight
    
    def save_book(self, filename):
        """Save opening book to file"""
        with open(filename, 'w') as f:
            json.dump(self.book, f, indent=2)
