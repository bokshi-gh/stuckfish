#pragma once

#include <vector>

#include "board.h"

class MoveGenerator {
public:
    static std::vector<Move> generateMoves(
        const Board& board
    );

private:
    static void generatePawnMoves(
        const Board& board,
        std::vector<Move>& moves,
        int row,
        int col
    );

    static void generateKnightMoves(
        std::vector<Move>& moves,
        int row,
        int col
    );

    static void generateBishopMoves(
        std::vector<Move>& moves,
        int row,
        int col
    );

    static void generateRookMoves(
        std::vector<Move>& moves,
        int row,
        int col
    );

    static void generateQueenMoves(
        std::vector<Move>& moves,
        int row,
        int col
    );

    static void generateKingMoves(
        std::vector<Move>& moves,
        int row,
        int col
    );
};
