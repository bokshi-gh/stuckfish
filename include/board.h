#pragma once

#include "piece.h"
#include "move.h"

class Board {
private:
    Piece squares[8][8];

public:
    Board();

    void initialize();

    Piece get(int row, int col) const;

    void set(int row, int col, Piece piece);

    void makeMove(const Move& move);

    void print() const;
};
