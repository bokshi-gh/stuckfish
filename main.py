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

def main():
    """Main entry point"""
    uci = UCI()
    uci.run()

if __name__ == "__main__":
    main()
