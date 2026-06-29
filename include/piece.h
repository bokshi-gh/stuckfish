#pragma once

enum class Color {
    WHITE = 0,
    BLACK = 1,
    NONE  = 2
};

enum class PieceType {
    NONE = 0,
    PAWN,
    KNIGHT,
    BISHOP,
    ROOK,
    QUEEN,
    KING
};

struct Piece {
    PieceType type = PieceType::NONE;
    Color color    = Color::NONE;

    bool isEmpty() const { 
        return type == PieceType::NONE; 
    }
};
