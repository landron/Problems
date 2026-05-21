/*
Solve Diagonal Sudoku with 3x3 Blocks using iterative DFS.
*/

#include <cassert>
#include <utility>
#include <vector>

#include <gtest/gtest.h>

#include "ext_8_diagonal_sudoku.h"

namespace {

auto is_valid(const Grid& grid, unsigned row, unsigned col, unsigned num)
    -> bool {
    assert(row < 9 && col < 9 && num > 0 && num < 10);

    for (size_t i = 0; i < 9; ++i) {
        if ((i != col && grid[row][i] == num) ||
            (i != row && grid[i][col] == num))
            return false;
    }

    for (size_t i = 0; i < 3; ++i) {
        for (size_t j = 0; j < 3; ++j) {
            if (i == row % 3 && j == col % 3) continue;
            if (grid[row - row % 3 + i][col - col % 3 + j] == num) return false;
        }
    }

    if (row == col) {
        for (size_t i = 0; i < 9; ++i) {
            if (i == row) continue;
            if (grid[i][i] == num) return false;
        }
    }

    if (row + col == 8) {
        for (size_t i = 0; i < 9; ++i) {
            if (i == row && (8 - i) == col) continue;
            if (grid[i][8 - i] == num) return false;
        }
    }

    return true;
}

auto is_valid_solution(const Grid& grid) -> bool {
    for (unsigned row = 0; row < 9; ++row) {
        for (unsigned col = 0; col < 9; ++col) {
            auto num = grid[row][col];
            if (num != 0 && !is_valid(grid, row, col, num)) return false;
        }
    }
    return true;
}

} // namespace

namespace diagonal_sudoku_dfs {

// Iterative DFS/backtracking: place a value, move to the next empty cell,
// and only when stuck backtrack to the previous cell to try the next value.
auto solve(const Grid& board) -> Grid {
    auto result = board;

    if (!is_valid_solution(result)) {
        return {};
    }

    std::vector<std::pair<size_t, size_t>> empty_cells;
    for (size_t row = 0; row < 9; ++row) {
        for (size_t col = 0; col < 9; ++col) {
            if (result[row][col] == 0) {
                empty_cells.emplace_back(row, col);
            }
        }
    }

    if (empty_cells.empty()) {
        return result;
    }

    std::vector<unsigned> next_num_to_try(empty_cells.size(), 1);
    size_t pos = 0;

    while (pos < empty_cells.size()) {
        auto [row, col] = empty_cells[pos];
        bool placed = false;

        for (unsigned num = next_num_to_try[pos]; num < 10; ++num) {
            if (is_valid(result, row, col, num)) {
                result[row][col] = num;
                next_num_to_try[pos] = num + 1;
                ++pos;
                if (pos < empty_cells.size()) {
                    next_num_to_try[pos] = 1;
                }
                placed = true;
                break;
            }
        }

        if (placed) {
            continue;
        }

        next_num_to_try[pos] = 1;
        result[row][col] = 0;

        if (pos == 0) {
            return {};
        }

        --pos;
        auto [prev_row, prev_col] = empty_cells[pos];
        result[prev_row][prev_col] = 0;
    }

    return result;
}

} // namespace diagonal_sudoku_dfs

// clang-format off

// Tests for diagonal_sudoku_dfs::solve
#define DFS_SOLVED_GRID \
    {1, 2, 3, 4, 5, 6, 7, 8, 9}, \
    {4, 5, 6, 7, 8, 9, 1, 2, 3}, \
    {7, 8, 9, 1, 2, 3, 4, 5, 6}, \
    {2, 1, 4, 3, 6, 5, 8, 9, 7}, \
    {3, 6, 8, 9, 7, 2, 5, 1, 4}, \
    {5, 9, 7, 8, 1, 4, 6, 3, 2}, \
    {9, 4, 1, 6, 3, 8, 2, 7, 5}, \
    {8, 3, 2, 5, 4, 7, 9, 6, 1}, \
    {6, 7, 5, 2, 9, 1, 3, 4, 8}

TEST(SolveDiagonalSudokuDFS, CompletedGrid) {
    Grid input    = {DFS_SOLVED_GRID};
    Grid expected = {DFS_SOLVED_GRID};
    EXPECT_EQ(diagonal_sudoku_dfs::solve(input), expected);
}

TEST(SolveDiagonalSudokuDFS, TwoEmptyCells) {
    Grid input = {{0, 2, 3, 4, 5, 6, 7, 8, 9},
                  {4, 5, 6, 7, 8, 9, 1, 2, 3},
                  {7, 8, 9, 1, 2, 3, 4, 5, 6},
                  {2, 1, 4, 3, 6, 5, 8, 9, 7},
                  {3, 6, 8, 9, 0, 2, 5, 1, 4},
                  {5, 9, 7, 8, 1, 4, 6, 3, 2},
                  {9, 4, 1, 6, 3, 8, 2, 7, 5},
                  {8, 3, 2, 5, 4, 7, 9, 6, 1},
                  {6, 7, 5, 2, 9, 1, 3, 4, 8}};
    Grid expected = {DFS_SOLVED_GRID};
    EXPECT_EQ(diagonal_sudoku_dfs::solve(input), expected);
}

TEST(SolveDiagonalSudokuDFS, InvalidPuzzleReturnsEmpty) {
    Grid input = {{1, 1, 0, 0, 0, 0, 0, 0, 0},
                  {0, 0, 0, 0, 0, 0, 0, 0, 0},
                  {0, 0, 0, 0, 0, 0, 0, 0, 0},
                  {0, 0, 0, 0, 0, 0, 0, 0, 0},
                  {0, 0, 0, 0, 0, 0, 0, 0, 0},
                  {0, 0, 0, 0, 0, 0, 0, 0, 0},
                  {0, 0, 0, 0, 0, 0, 0, 0, 0},
                  {0, 0, 0, 0, 0, 0, 0, 0, 0},
                  {0, 0, 0, 0, 0, 0, 0, 0, 0}};

    EXPECT_TRUE(diagonal_sudoku_dfs::solve(input).empty());
}

// clang-format on
