#pragma once

#include "piece.h"

struct Move {
    int fromRow;
    int fromCol;

    int toRow;
    int toCol;

    bool capture;
    bool doublePawnPush;
    bool enPassant;
    bool castleKingside;
    bool castleQueenside;

    Piece promotion;
};
