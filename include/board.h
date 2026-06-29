#pragma once

#include <utility>
#include "piece.h"
#include "move.h"

class Board {
private:
    Piece squares[8][8];

public:
    Board();

    Piece getPiece(int row, int col) const;
    void setPiece(int row, int col, Piece piece);

    bool onBoard(int row, int col) const;

    void printBoard() const;

    void makeMove(const Move& move);
    void undoMove(const Move& move, Piece captured);

    std::pair<int,int> kingSquare(Color color) const;

    bool isSquareAttacked(
        int row,
        int col,
        Color attacker
    ) const;

    bool isKingInCheck(Color color) const;
};
