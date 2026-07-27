# Stuckfish Chess Engine

A UCI-compliant chess engine written in Python.

## Quick Start

```bash
git clone https://github.com/bokshi-gh/stuckfish.git
cd stuckfish
python main.py
```

## Features

- ✅ UCI Protocol Support - Works with any UCI-compatible chess GUI
- ✅ Bitboard Representation - Efficient board representation
- ✅ Legal Move Generation - Complete move generation for all pieces
- ✅ Alpha-Beta Search - Minimax search with alpha-beta pruning
- ✅ Iterative Deepening - Progressive search depth
- ✅ Position Evaluation - Material and positional evaluation
- ✅ FEN Support - Parse and generate FEN strings
- ✅ No Dependencies - Pure Python, no external libraries needed

## Usage

### As a UCI Engine

```bash
python main.py
```

### In a Chess GUI

1. Open your UCI-compatible chess GUI (Arena, Cute Chess, Fritz, etc.)
2. Add a new engine pointing to `main.py`
3. Start playing!

### Programmatic Usage

```python
from engine.board import Board
from engine.search import Search

board = Board()
search = Search(board)
best_move, score = search.search(depth=4)
print(f"Best move: {best_move}")
```

## Project Structure

```
stuckfish/
├── main.py               # Entry point
├── engine/
│   ├── __init__.py
│   ├── board.py          # Board representation
│   ├── movegen.py        # Move generation
│   ├── search.py         # Search algorithms
│   ├── evaluation.py     # Position evaluation
│   ├── uci.py            # UCI protocol
│   ├── bitboard.py       # Bitboard utilities
│   └── constants.py      # Game constants
├── LICENSE               # License file
└── README.md             # Project documentation
```

## UCI Commands

- `uci` - Identify the engine
- `isready` - Check if engine is ready  
- `ucinewgame` - Reset engine
- `position` - Set up a position
- `go` - Start search
- `stop` - Stop search
- `quit` - Quit engine
- `d` - Display board

## Performance

- 1,000-10,000 nodes per second
- Depth 4-6 in 1-5 seconds
- Educational engine, not for competitive play

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for more information.

## Connect

- GitHub: [bokshi-gh](https://github.com/bokshi-gh)
- Email: devrajeshthapa@gmail.com

## Testing with a Chess GUI

1. Download a UCI-compatible GUI like [Arena](http://www.playwitharena.com/) or [Cute Chess](https://cutechess.com/)
2. Add a new engine
3. Point to `python.exe` as the command and `main.py` as the parameter
4. Or create a batch file `run.bat`:
```batch
@echo off
python main.py
```
