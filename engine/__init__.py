"""
Stuckfish Chess Engine
A UCI-compliant chess engine
Author: Rajesh Thapa (bokshi)
"""

__version__ = "2.0.0"
__author__ = "Rajesh Thapa (bokshi)"

from .board import Board
from .search import Search
from .uci import UCI
from .transposition import TranspositionTable
