#include "board.h"

#include <iostream>
#include <cctype>

Board::Board() {

    for (int r = 0; r < 8; r++) {
        for (int c = 0; c < 8; c++) {
            squares[r][c] = {};
        }
    }
}

Piece Board::getPiece(
    int row,
    int col
) const {

    return squares[row][col];
}

void Board::setPiece(
    int row,
    int col,
    Piece piece
) {

    squares[row][col] = piece;
}

bool Board::onBoard(
    int row,
    int col
) const {

    return row >= 0 &&
           row < 8 &&
           col >= 0 &&
           col < 8;
}

void Board::printBoard() const {

    for (int r = 0; r < 8; r++) {

        for (int c = 0; c < 8; c++) {

            Piece p =
                squares[r][c];

            char ch = '.';

            switch (p.type) {

                case PieceType::PAWN:
                    ch = 'P';
                    break;

                case PieceType::KNIGHT:
                    ch = 'N';
                    break;

                case PieceType::BISHOP:
                    ch = 'B';
                    break;

                case PieceType::ROOK:
                    ch = 'R';
                    break;

                case PieceType::QUEEN:
                    ch = 'Q';
                    break;

                case PieceType::KING:
                    ch = 'K';
                    break;

                default:
                    break;
            }

            if (p.color ==
                Color::BLACK) {

                ch =
                    std::tolower(ch);
            }

            std::cout
                << ch
                << ' ';
        }

        std::cout
            << '\n';
    }
}

void Board::makeMove(
    const Move& move
) {

    Piece moving =
        getPiece(
            move.fromRow,
            move.fromCol
        );

    setPiece(
        move.toRow,
        move.toCol,
        moving
    );

    setPiece(
        move.fromRow,
        move.fromCol,
        {}
    );

    if (
        move.promotion.type
        !=
        PieceType::NONE
    ) {

        setPiece(
            move.toRow,
            move.toCol,
            move.promotion
        );
    }
}

void Board::undoMove(
    const Move& move,
    Piece captured
) {

    Piece moving =
        getPiece(
            move.toRow,
            move.toCol
        );

    setPiece(
        move.fromRow,
        move.fromCol,
        moving
    );

    setPiece(
        move.toRow,
        move.toCol,
        captured
    );
}

std::pair<int,int>
Board::kingSquare(
    Color color
) const {

    for (
        int r = 0;
        r < 8;
        r++
    ) {

        for (
            int c = 0;
            c < 8;
            c++
        ) {

            Piece p =
                squares[r][c];

            if (
                p.type ==
                PieceType::KING
                &&
                p.color ==
                color
            ) {

                return {
                    r,
                    c
                };
            }
        }
    }

    return {
        -1,
        -1
    };
}

bool Board::isSquareAttacked(
    int row,
    int col,
    Color attacker
) const {

    auto slide =
        [&](

        const int dr[],
        const int dc[],
        int count,

        PieceType a,
        PieceType b

        ) {

        for (
            int i = 0;
            i < count;
            i++
        ) {

            int r =
                row +
                dr[i];

            int c =
                col +
                dc[i];

            while (
                onBoard(
                    r,
                    c
                )
            ) {

                Piece p =
                    getPiece(
                        r,
                        c
                    );

                if (
                    !p.isEmpty()
                ) {

                    if (
                        p.color ==
                        attacker
                        &&
                        (
                        p.type
                        ==
                        a
                        ||
                        p.type
                        ==
                        b
                        )
                    ) {

                        return true;
                    }

                    break;
                }

                r += dr[i];
                c += dc[i];
            }
        }

        return false;
    };

    // PAWN

    int pawnRow =
        attacker ==
        Color::WHITE
        ? row + 1
        : row - 1;

    if (
        onBoard(
            pawnRow,
            col - 1
        )
    ) {

        Piece p =
            getPiece(
                pawnRow,
                col - 1
            );

        if (
            p.type ==
            PieceType::PAWN
            &&
            p.color ==
            attacker
        ) {

            return true;
        }
    }

    if (
        onBoard(
            pawnRow,
            col + 1
        )
    ) {

        Piece p =
            getPiece(
                pawnRow,
                col + 1
            );

        if (
            p.type ==
            PieceType::PAWN
            &&
            p.color ==
            attacker
        ) {

            return true;
        }
    }

    // KNIGHT

    int knr[8] =
    {
        -2,-2,
        -1,-1,
         1, 1,
         2, 2
    };

    int knc[8] =
    {
        -1,1,
        -2,2,
        -2,2,
        -1,1
    };

    for (
        int i = 0;
        i < 8;
        i++
    ) {

        int r =
            row +
            knr[i];

        int c =
            col +
            knc[i];

        if (
            !onBoard(
                r,
                c
            )
        ) {
            continue;
        }

        Piece p =
            getPiece(
                r,
                c
            );

        if (
            p.type ==
            PieceType::KNIGHT
            &&
            p.color ==
            attacker
        ) {

            return true;
        }
    }

    // BISHOP / QUEEN

    {
        int dr[4] =
        {
            -1,-1,
             1, 1
        };

        int dc[4] =
        {
            -1,1,
            -1,1
        };

        if (
            slide(
                dr,
                dc,
                4,
                PieceType::BISHOP,
                PieceType::QUEEN
            )
        ) {

            return true;
        }
    }

    // ROOK / QUEEN

    {
        int dr[4] =
        {
            -1,
             1,
             0,
             0
        };

        int dc[4] =
        {
             0,
             0,
            -1,
             1
        };

        if (
            slide(
                dr,
                dc,
                4,
                PieceType::ROOK,
                PieceType::QUEEN
            )
        ) {

            return true;
        }
    }

    // KING

    for (
        int dr = -1;
        dr <= 1;
        dr++
    ) {

        for (
            int dc = -1;
            dc <= 1;
            dc++
        ) {

            if (
                dr == 0
                &&
                dc == 0
            )
                continue;

            int r =
                row +
                dr;

            int c =
                col +
                dc;

            if (
                !onBoard(
                    r,
                    c
                )
            )
                continue;

            Piece p =
                getPiece(
                    r,
                    c
                );

            if (
                p.type ==
                PieceType::KING
                &&
                p.color ==
                attacker
            ) {

                return true;
            }
        }
    }

    return false;
}

bool Board::isKingInCheck(
    Color color
) const {

    auto king =
        kingSquare(
            color
        );

    if (
        king.first
        ==
        -1
    ) {

        return false;
    }

    Color enemy =
        color ==
        Color::WHITE
        ? Color::BLACK
        : Color::WHITE;

    return
        isSquareAttacked(
            king.first,
            king.second,
            enemy
        );
}
