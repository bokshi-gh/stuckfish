"""
Stuckfish Chess Engine
A UCI-compliant chess engine
"""

from .constants import ENGINE_NAME, ENGINE_VERSION, ENGINE_AUTHOR
from .board import Board
from .search import Search
from .uci import UCI
from .transposition import TranspositionTable
from .zobrist import Zobrist

__version__ = ENGINE_VERSION
__author__ = ENGINE_AUTHOR
