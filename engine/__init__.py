"""
Stuckfish Chess Engine
A UCI-compliant chess engine
Author: Rajesh Thapa (bokshi)
"""

from .constants import ENGINE_NAME, ENGINE_VERSION, ENGINE_AUTHOR
from .board import Board
from .search import Search
from .uci import UCI
from .transposition import TranspositionTable

__version__ = ENGINE_VERSION
__author__ = ENGINE_AUTHOR
