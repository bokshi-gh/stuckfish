#include "board.h"

#include <iostream>

Board::Board() {
    initialize();
}

void Board::initialize() {

    // Clear board
    for (int row = 0; row < 8; row++) {
        for (int col = 0; col < 8; col++) {
            squares[row][col] =
                Piece::EMPTY;
        }
    }

    // Black major pieces

    squares[0][0] =
    squares[0][7] =
        Piece::BLACK_ROOK;

    squares[0][1] =
    squares[0][6] =
        Piece::BLACK_KNIGHT;

    squares[0][2] =
    squares[0][5] =
        Piece::BLACK_BISHOP;

    squares[0][3] =
        Piece::BLACK_QUEEN;

    squares[0][4] =
        Piece::BLACK_KING;

    // Black pawns

    for (int col = 0; col < 8; col++) {
        squares[1][col] =
            Piece::BLACK_PAWN;
    }

    // White major pieces

    squares[7][0] =
    squares[7][7] =
        Piece::WHITE_ROOK;

    squares[7][1] =
    squares[7][6] =
        Piece::WHITE_KNIGHT;

    squares[7][2] =
    squares[7][5] =
        Piece::WHITE_BISHOP;

    squares[7][3] =
        Piece::WHITE_QUEEN;

    squares[7][4] =
        Piece::WHITE_KING;

    // White pawns

    for (int col = 0; col < 8; col++) {
        squares[6][col] =
            Piece::WHITE_PAWN;
    }
}

Piece Board::get(
    int row,
    int col
) const {

    return squares[row][col];
}

void Board::set(
    int row,
    int col,
    Piece piece
) {

    squares[row][col] =
        piece;
}

void Board::print() const {

    auto symbol =
        [](Piece piece) {

        switch (piece) {

            case Piece::WHITE_PAWN:
                return 'P';

            case Piece::WHITE_KNIGHT:
                return 'N';

            case Piece::WHITE_BISHOP:
                return 'B';

            case Piece::WHITE_ROOK:
                return 'R';

            case Piece::WHITE_QUEEN:
                return 'Q';

            case Piece::WHITE_KING:
                return 'K';

            case Piece::BLACK_PAWN:
                return 'p';

            case Piece::BLACK_KNIGHT:
                return 'n';

            case Piece::BLACK_BISHOP:
                return 'b';

            case Piece::BLACK_ROOK:
                return 'r';

            case Piece::BLACK_QUEEN:
                return 'q';

            case Piece::BLACK_KING:
                return 'k';

            default:
                return '.';
        }
    };

    for (int row = 0; row < 8; row++) {

        for (int col = 0; col < 8; col++) {

            std::cout
                << symbol(
                    squares[row][col]
                )
                << " ";

        }

        std::cout
            << "\n";
    }
}
