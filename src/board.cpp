#include "board.h"

#include <iostream>

static Piece makePiece(
    PieceType type,
    Color color
) {
    return {type, color};
}

Board::Board() {

    // White back row

    squares[0] = makePiece(PieceType::ROOK, Color::WHITE);
    squares[1] = makePiece(PieceType::KNIGHT, Color::WHITE);
    squares[2] = makePiece(PieceType::BISHOP, Color::WHITE);
    squares[3] = makePiece(PieceType::QUEEN, Color::WHITE);
    squares[4] = makePiece(PieceType::KING, Color::WHITE);
    squares[5] = makePiece(PieceType::BISHOP, Color::WHITE);
    squares[6] = makePiece(PieceType::KNIGHT, Color::WHITE);
    squares[7] = makePiece(PieceType::ROOK, Color::WHITE);

    // White pawns

    for (int i = 8; i < 16; i++) {
        squares[i] =
            makePiece(
                PieceType::PAWN,
                Color::WHITE
            );
    }

    // Black pawns

    for (int i = 48; i < 56; i++) {
        squares[i] =
            makePiece(
                PieceType::PAWN,
                Color::BLACK
            );
    }

    // Black back row

    squares[56] = makePiece(PieceType::ROOK, Color::BLACK);
    squares[57] = makePiece(PieceType::KNIGHT, Color::BLACK);
    squares[58] = makePiece(PieceType::BISHOP, Color::BLACK);
    squares[59] = makePiece(PieceType::QUEEN, Color::BLACK);
    squares[60] = makePiece(PieceType::KING, Color::BLACK);
    squares[61] = makePiece(PieceType::BISHOP, Color::BLACK);
    squares[62] = makePiece(PieceType::KNIGHT, Color::BLACK);
    squares[63] = makePiece(PieceType::ROOK, Color::BLACK);
}

char Board::pieceSymbol(const Piece& p) {
    if (p.type == PieceType::NONE)
        return '.';

    bool white =
        p.color ==
        Color::WHITE;

    switch (p.type) {

        case PieceType::PAWN:
            return white ? 'P' : 'p';

        case PieceType::KNIGHT:
            return white ? 'N' : 'n';

        case PieceType::BISHOP:
            return white ? 'B' : 'b';

        case PieceType::ROOK:
            return white ? 'R' : 'r';

        case PieceType::QUEEN:
            return white ? 'Q' : 'q';

        case PieceType::KING:
            return white ? 'K' : 'k';

        default:
            return '.';
    }
}

void Board::print() const {

    for (int row = 7; row >= 0; row--) {

        for (int col = 0; col < 8; col++) {

            std::cout
                << pieceSymbol(
                    squares[
                        row * 8 + col
                    ]
                )
                << ' ';
        }

        std::cout << '\n';
    }
}
