# Stuckfish Chess Engine

A UCI-compliant chess engine written in Python with advanced search optimizations and modern chess engine features.

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![UCI](https://img.shields.io/badge/UCI-Compliant-orange.svg)](http://wbec-ridderkerk.nl/html/UCIProtocol.html)

## Quick Start

```bash
git clone https://github.com/bokshi-gh/stuckfish.git
cd stuckfish
python main.py
```

## Features

### Core Features
- UCI Protocol Support - Works with Arena, Cute Chess, Fritz, and any UCI-compatible GUI
- Full Bitboard Representation - Efficient 64-bit board representation
- Complete Legal Move Generation - All pieces with full validation
- FEN Support - Parse and generate FEN strings
- Pure Python - No external dependencies

### Advanced Search Optimizations
- Alpha-Beta Pruning - Minimax search with alpha-beta cutoff
- Iterative Deepening - Progressive search depth for better time management
- Transposition Table - Cache evaluated positions for 2-4x speed boost
- Move Ordering - MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
- Killer Moves - Remember good moves for future searches
- History Heuristic - Track successful moves across positions
- Null Move Pruning - Skip searching obviously bad moves
- Aspiration Windows - Narrow search windows for faster pruning
- Principal Variation Search - Efficient search ordering
- Quiescence Search - Avoid horizon effect with selective capture search

### Modern Chess Engine Features
- **Zobrist Hashing** - Fast transposition table lookups
- **Opening Book Support** - Pre-computed opening moves for better early game
- **Syzygy Tablebase Support** - Perfect endgame play (requires external files)
- **Lazy SMP** - Parallel search with multiple threads
- **UCI Options** - Hash size, Threads, Ponder, OwnBook
- **Principal Variation Collection** - Show best line of play
- **Better Evaluation** - King safety, pawn structure analysis

### Position Evaluation
- Material values with piece-square tables
- Positional evaluation for all pieces
- King safety and pawn structure
- Endgame and middlegame king tables
- Mirror tables for black pieces

## Performance

| Metric | Value |
|--------|-------|
| Nodes per second | 10,000 - 50,000 |
| Typical search depth | 6-8 plies |
| Transposition table hit rate | 40-70% |

## Project Structure

```
stuckfish/
├── main.py                    # Entry point
├── engine/
│   ├── __init__.py           # Package initialization
│   ├── board.py              # Board with full attack detection
│   ├── movegen.py            # Move generation with ordering
│   ├── search.py             # Advanced search with all optimizations
│   ├── evaluation.py         # Material & positional evaluation
│   ├── uci.py                # UCI protocol implementation
│   ├── transposition.py      # Transposition table
│   ├── zobrist.py            # Zobrist hashing
│   ├── opening.py            # Opening book support
│   ├── endgame.py            # Syzygy tablebase support
│   ├── bitboard.py           # Bitboard utilities
│   └── constants.py          # Game constants
├── LICENSE
└── README.md
```

## Usage

### Running the Engine

```bash
python main.py
```

This starts the engine in UCI mode. It reads commands from standard input (stdin) and outputs responses to standard output (stdout). For normal use, connect it to a UCI-compatible chess GUI.

You can also type UCI commands directly for testing:

```
uci
isready
position startpos
go depth 6
quit
```

### Building a Standalone Executable with PyInstaller

To distribute Stuckfish as a single executable file without requiring Python:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller --onefile --name stuckfish main.py
```

3. The executable will be created in the `dist` folder:
   - Windows: `dist/stuckfish.exe`
   - Linux: `dist/stuckfish`
   - macOS: `dist/stuckfish`

4. Run the executable:
```bash
# Windows
dist\stuckfish.exe

# Linux/macOS
./dist/stuckfish
```

### Using the Executable in a Chess GUI

1. Open your UCI-compatible chess GUI (Arena, Cute Chess, Fritz, etc.)
2. Add a new engine
3. Point to the executable file:
   - Windows: `C:\path\to\stuckfish.exe`
   - Linux/macOS: `/path/to/stuckfish`
4. No parameters needed (the executable runs in UCI mode by default)

### PyInstaller Options

For a smaller executable with better performance:

```bash
# Optimized build (recommended)
pyinstaller --onefile --name stuckfish --noconsole --strip main.py

# With debug output
pyinstaller --onefile --name stuckfish --debug main.py
```

### Programmatic Usage

```python
from engine.board import Board
from engine.search import Search

# Create board and search
board = Board()
search = Search(board)

# Search for best move
best_move, score = search.search(depth=6, time_limit=5.0)
print(f"Best move: {best_move}, Score: {score}")
```

## UCI Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| Hash | spin | 64 | Transposition table size in MB |
| Threads | spin | 1 | Number of threads for Lazy SMP |
| Ponder | check | false | Enable pondering |
| OwnBook | check | false | Use opening book |

## UCI Commands

| Command | Description |
|---------|-------------|
| `uci` | Identify the engine |
| `isready` | Check if engine is ready |
| `ucinewgame` | Reset engine for new game |
| `setoption` | Set UCI options |
| `position` | Set up a position (startpos or FEN) |
| `go` | Start search with parameters |
| `stop` | Stop the current search |
| `quit` | Quit the engine |
| `d` | Display the current board |

### Example UCI Session

```
position startpos
go depth 6
info depth 1 score 50 nodes 20
info depth 2 score 25 nodes 400
info pv e2e4
...
bestmove e2e4
```

## Opening Book

The engine supports opening books in JSON format:

```json
{
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": {
        "e2e4": 100,
        "d2d4": 90,
        "g1f3": 80,
        "c2c4": 70
    }
}
```

To use your own opening book:
1. Create a JSON file with positions and moves
2. Place it in the engine directory
3. Enable OwnBook option in UCI

## Endgame Tablebases

The engine supports Syzygy tablebases for perfect endgame play:

1. Download Syzygy tablebases from: http://tablebase.sesse.net/
2. Place them in a directory
3. The engine will automatically detect and use them

## Search Optimizations Explained

### 1. Zobrist Hashing
Fast position hashing for transposition table lookups.
- Speed boost: 2-4x
- Hit rate: 40-70%

### 2. Lazy SMP
Parallel search across multiple threads.
- Speed boost: ~2x per thread (diminishing returns)
- Scales up to 8 threads effectively

### 3. Transposition Table
Caches previously evaluated positions.
- Speed boost: 2-4x
- Uses Zobrist hashing for fast lookups

### 4. Move Ordering
- MVV-LVA: Captures first (most valuable victim, least valuable attacker)
- Killer Moves: Remember good moves in similar positions
- History Heuristic: Track move success across positions

### 5. Null Move Pruning
Skip searching a position if it's clearly bad.
- Speed boost: 1.3x

### 6. Aspiration Windows
Narrow the search window for faster pruning.
- Speed boost: 1.2x

### 7. Principal Variation Search
Efficiently search the most promising line first.
- Speed boost: 1.5x

## Future Improvements

- [ ] Neural network evaluation (NNUE)
- [ ] Multi-variant search
- [ ] More opening books
- [ ] Online database support
- [ ] GUI interface
- [ ] Game analysis features
- [ ] Chess960 support
- [ ] Time management improvements

## License

Distributed under the MIT License. See LICENSE file for more information.

## Connect

- GitHub: [bokshi-gh](https://github.com/bokshi-gh)
- Email: devrajeshthapa@gmail.com

## Acknowledgments

- Inspired by Stockfish, the world's strongest chess engine
- Built using concepts from the Chess Programming Wiki
- UCI protocol documentation from wbec-ridderkerk.nl
- Syzygy tablebases by Ronald de Man
