#!/usr/bin/env python
"""
Stuckfish - A UCI-compliant chess engine
Author: Rajesh Thapa (bokshi)
"""

import sys
import os

# Add the engine directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'engine'))

from engine.uci import UCI
from engine.perft import Perft
from engine.board import Board

def run_uci():
    """Run in UCI mode"""
    uci = UCI()
    uci.run()

def run_perft(depth):
    """Run perft test"""
    board = Board()
    perft = Perft(board)
    total = perft.run_perft(depth)
    print(f"\nTotal nodes: {total}")
    return total

def main():
    """Main entry point"""
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--perft" and len(sys.argv) > 2:
            try:
                depth = int(sys.argv[2])
                return run_perft(depth)
            except ValueError:
                print("Invalid depth for perft")
                return 1
        elif sys.argv[1] in ["-h", "--help"]:
            print("Stuckfish Chess Engine")
            print("Author: Rajesh Thapa (bokshi)")
            print("\nUsage:")
            print("  python main.py [OPTIONS]")
            print("\nOptions:")
            print("  -u, --uci      Run in UCI mode (default)")
            print("  --perft DEPTH  Run perft test at specified depth")
            print("  -h, --help     Show this help message")
            print("  --version      Show version information")
            return 0
        elif sys.argv[1] == "--version":
            print("Stuckfish Chess Engine v1.0.0")
            print("Author: Rajesh Thapa (bokshi)")
            return 0
    
    # Default: UCI mode
    run_uci()

if __name__ == "__main__":
    main()
