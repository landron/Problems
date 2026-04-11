/*
Solve Diagonal Sudoku with 3x3 Blocks
Given a 9x9 grid with empty cells marked as 0, fill the grid so that each row,
column, 3x3 block, and both main diagonals contain numbers 1 to 9 exactly once.
https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/solve-diagonal-sudoku-3x3-blocks
    Hackerrank tests are poorly written: if invalid input, just return the
input! So return board; instead of return {};
*/

#include <optional>
#include <print>
#include <ranges>
#include <stack>
#include <vector>

#include <gtest/gtest.h>

#include "ext_8_diagonal_sudoku.h"

enum class Validity : unsigned {
    Valid = 0,
    RowColConflict = 1,
    BlockConflict = 2,
    MainDiagonalConflict = 3,
    AntiDiagonalConflict = 4
};

auto is_valid(const Grid& grid, unsigned row, unsigned col, unsigned num,
              bool print_it = false) -> Validity {
    assert(row < 9 && col < 9 && num > 0 && num < 10);

    if (print_it)
        std::println("Checking if {} can be placed at ({}, {})", num, row, col);

    for (size_t i = 0; i < 9; ++i) {
        if ((i != col && grid[row][i] == num) ||
            (i != row && grid[i][col] == num)) {
            if (print_it) std::println("... row/col exists");
            return Validity::RowColConflict;
        }
    }

    for (size_t i = 0; i < 3; ++i) {
        for (size_t j = 0; j < 3; ++j) {
            if (i == row % 3 && j == col % 3) continue;
            if (grid[row - row % 3 + i][col - col % 3 + j] == num) {
                if (print_it) std::println("... 3x3 block exists");
                return Validity::BlockConflict;
            }
        }
    }

    if (row == col) { // Main diagonal
        for (size_t i = 0; i < 9; ++i) {
            if (i == row) continue;
            if (grid[i][i] == num) {
                if (print_it) std::println("... main diagonal exists");
                return Validity::MainDiagonalConflict;
            }
        }
    }
    if (row + col == 8) { // Anti-diagonal
        for (size_t i = 0; i < 9; ++i) {
            if (i == row && (8 - i) == col) continue;
            if (grid[i][8 - i] == num) {
                if (print_it) std::println("... anti-diagonal exists");
                return Validity::AntiDiagonalConflict;
            }
        }
    }

    return Validity::Valid;
};

auto solve_diagonal_sudoku(const Grid& board) -> Grid {
    auto find_next_empty =
        [](const Grid& grid, size_t start_row,
           size_t start_col) -> std::optional<std::pair<size_t, size_t>> {
        for (size_t row = start_row; row < 9; ++row) {
            for (size_t col = (row == start_row) ? start_col : 0; col < 9;
                 ++col) {
                if (grid[row][col] == 0) {
                    return {{row, col}};
                }
            }
        }
        return std::nullopt;
    };

    auto result = board;
    // (row, col, next_num_to_try)
    std::stack<std::tuple<size_t, size_t, size_t>> backtrack;
    auto current_search = std::tuple<size_t, size_t, size_t>{0, 0, 1};

    while (true) {
        auto [i, j, num] = current_search;

        if (auto next_empty = find_next_empty(result, i, j); !next_empty) {
            // All cells filled: solution found
            return result;
        } else {
            // THE OLD (C++11) WAY - Ugly, use only for re-assignment
            std::tie(i, j) = *next_empty;
        }

        // Try values from num to 9 for this cell
        for (; num < 10; ++num) {
            if (is_valid(result, i, j, num) == Validity::Valid) {
                result[i][j] = num;
                backtrack.push({i, j, num + 1});
                // Continue search (next empty cell) from current position)
                current_search = {i, j, 1};
                break;
            }
        }

        if (num == 10) {
            // No valid number 1-9: backtrack
            if (backtrack.empty()) {
                break; // No solution exists
            }
            auto [prev_i, prev_j, prev_num] = backtrack.top();
            result[prev_i][prev_j] = 0; // Clear cell for retry
            current_search = backtrack.top();
            backtrack.pop();
        }
    }

    return {};
}

using GridHKR = std::vector<std::vector<int>>;
GridHKR completeDiagonalSudokuGrid(const GridHKR& grid_in) {
    Grid grid;
    for (const auto& row : grid_in) {
        std::vector<unsigned> new_row;
        for (int cell : row) {
            new_row.push_back(static_cast<unsigned>(cell));
        }
        grid.push_back(std::move(new_row));
    }

    auto solved = solve_diagonal_sudoku(grid);
    if (0) {
        if (solved.empty()) {
            std::cout << "No solution exists for the given grid." << std::endl;
            return {};
        }
        std::cout << "Solved grid:" << std::endl;
        for (const auto& row : solved) {
            for (auto cell : row) {
                std::cout << cell << " ";
            }
            std::cout << std::endl;
        }
    }

    GridHKR grid_out;
    for (const auto& row : solved) {
        std::vector<int> new_row;
        for (unsigned cell : row) {
            new_row.push_back(static_cast<int>(cell));
        }
        grid_out.push_back(std::move(new_row));
    }
    return grid_out;
}

auto is_valid_diagonal_sudoku(const Grid& grid, bool print_it = false)
    -> std::tuple<unsigned, unsigned, unsigned, Validity> {
    for (unsigned row = 0; row < 9; ++row) {
        for (unsigned col = 0; col < 9; ++col) {
            unsigned num = grid[row][col];
            if (num != 0) {
                auto valid = is_valid(grid, row, col, num, print_it);
                if (valid != Validity::Valid) {
                    return {row, col, num, valid};
                }
            }
        }
    }
    return {};
}

// clang-format off

// Valid diagonal sudoku solution (rows, cols, 3x3 blocks, both diagonals all contain 1-9):
// Main diag: 1,5,9,3,7,4,2,6,8 | Anti diag: 9,9... wait verified by solver
#define SOLVED_GRID \
    {1, 2, 3, 4, 5, 6, 7, 8, 9}, \
    {4, 5, 6, 7, 8, 9, 1, 2, 3}, \
    {7, 8, 9, 1, 2, 3, 4, 5, 6}, \
    {2, 1, 4, 3, 6, 5, 8, 9, 7}, \
    {3, 6, 8, 9, 7, 2, 5, 1, 4}, \
    {5, 9, 7, 8, 1, 4, 6, 3, 2}, \
    {9, 4, 1, 6, 3, 8, 2, 7, 5}, \
    {8, 3, 2, 5, 4, 7, 9, 6, 1}, \
    {6, 7, 5, 2, 9, 1, 3, 4, 8}

TEST(SolveDiagonalSudoku, CompletedGrid) {
    Grid input    = {SOLVED_GRID};
    Grid expected = {SOLVED_GRID};
    EXPECT_EQ(solve_diagonal_sudoku(input), expected);
    // Also test iterative DFS variant
    EXPECT_EQ(diagonal_sudoku_dfs::solve(input), expected);
}

TEST(SolveDiagonalSudoku, AlmostCompletedGrid) {
    Grid input = {{1, 2, 3, 4, 5, 6, 7, 8, 9},
                  {4, 5, 6, 7, 8, 9, 1, 2, 3},
                  {7, 8, 9, 1, 2, 3, 4, 5, 6},
                  {2, 1, 4, 3, 6, 5, 8, 9, 7},
                  {3, 6, 8, 9, 7, 2, 5, 1, 4},
                  {5, 9, 7, 8, 1, 4, 6, 3, 2},
                  {9, 4, 1, 6, 3, 8, 2, 7, 5},
                  {8, 3, 2, 5, 4, 7, 9, 6, 1},
                  {6, 7, 5, 2, 9, 1, 3, 4, 0}}; // last cell empty

    Grid expected = {SOLVED_GRID};
    EXPECT_EQ(solve_diagonal_sudoku(input), expected);
    // Also test iterative DFS variant
    EXPECT_EQ(diagonal_sudoku_dfs::solve(input), expected);
}

TEST(SolveDiagonalSudoku, EmptyCellAtTopLeft) {
    Grid input = {{0, 2, 3, 4, 5, 6, 7, 8, 9},
                  {4, 5, 6, 7, 8, 9, 1, 2, 3},
                  {7, 8, 9, 1, 2, 3, 4, 5, 6},
                  {2, 1, 4, 3, 6, 5, 8, 9, 7},
                  {3, 6, 8, 9, 7, 2, 5, 1, 4},
                  {5, 9, 7, 8, 1, 4, 6, 3, 2},
                  {9, 4, 1, 6, 3, 8, 2, 7, 5},
                  {8, 3, 2, 5, 4, 7, 9, 6, 1},
                  {6, 7, 5, 2, 9, 1, 3, 4, 8}};

    Grid expected = {SOLVED_GRID};
    EXPECT_EQ(solve_diagonal_sudoku(input), expected);
    // Also test iterative DFS variant
    EXPECT_EQ(diagonal_sudoku_dfs::solve(input), expected);
}

TEST(SolveDiagonalSudoku, EmptyCellAtCenter) {
    // (4,4) is on the main diagonal
    Grid input = {{1, 2, 3, 4, 5, 6, 7, 8, 9},
                  {4, 5, 6, 7, 8, 9, 1, 2, 3},
                  {7, 8, 9, 1, 2, 3, 4, 5, 6},
                  {2, 1, 4, 3, 6, 5, 8, 9, 7},
                  {3, 6, 8, 9, 0, 2, 5, 1, 4},
                  {5, 9, 7, 8, 1, 4, 6, 3, 2},
                  {9, 4, 1, 6, 3, 8, 2, 7, 5},
                  {8, 3, 2, 5, 4, 7, 9, 6, 1},
                  {6, 7, 5, 2, 9, 1, 3, 4, 8}};

    Grid expected = {SOLVED_GRID};
    EXPECT_EQ(solve_diagonal_sudoku(input), expected);
    // Also test iterative DFS variant
    EXPECT_EQ(diagonal_sudoku_dfs::solve(input), expected);
}

TEST(SolveDiagonalSudoku, EmptyCellAtTopRight) {
    // (0,8) is on the anti-diagonal
    Grid input = {{1, 2, 3, 4, 5, 6, 7, 8, 0},
                  {4, 5, 6, 7, 8, 9, 1, 2, 3},
                  {7, 8, 9, 1, 2, 3, 4, 5, 6},
                  {2, 1, 4, 3, 6, 5, 8, 9, 7},
                  {3, 6, 8, 9, 7, 2, 5, 1, 4},
                  {5, 9, 7, 8, 1, 4, 6, 3, 2},
                  {9, 4, 1, 6, 3, 8, 2, 7, 5},
                  {8, 3, 2, 5, 4, 7, 9, 6, 1},
                  {6, 7, 5, 2, 9, 1, 3, 4, 8}};

    Grid expected = {SOLVED_GRID};
    EXPECT_EQ(solve_diagonal_sudoku(input), expected);
    // Also test iterative DFS variant
    EXPECT_EQ(diagonal_sudoku_dfs::solve(input), expected);
}

TEST(SolveDiagonalSudoku, TwoEmptyCells) {
    Grid input = {{0, 2, 3, 4, 5, 6, 7, 8, 9},
                  {4, 5, 6, 7, 8, 9, 1, 2, 3},
                  {7, 8, 9, 1, 2, 3, 4, 5, 6},
                  {2, 1, 4, 3, 6, 5, 8, 9, 7},
                  {3, 6, 8, 9, 0, 2, 5, 1, 4},
                  {5, 9, 7, 8, 1, 4, 6, 3, 2},
                  {9, 4, 1, 6, 3, 8, 2, 7, 5},
                  {8, 3, 2, 5, 4, 7, 9, 6, 1},
                  {6, 7, 5, 2, 9, 1, 3, 4, 8}};

    Grid expected = {SOLVED_GRID};
    EXPECT_EQ(solve_diagonal_sudoku(input), expected);
    // Also test iterative DFS variant
    EXPECT_EQ(diagonal_sudoku_dfs::solve(input), expected);
}

/*
1065 ms

./ctci-2026 --gtest_also_run_disabled_tests
*/
TEST(SolveDiagonalSudoku, DISABLED_HardPuzzle) {
    Grid input = {{0, 0, 0, 6, 0, 0, 0, 0, 0},
                  {0, 0, 2, 0, 0, 0, 0, 0, 8},
                  {0, 0, 0, 0, 4, 0, 0, 0, 0},
                  {0, 5, 0, 0, 0, 0, 0, 1, 0},
                  {0, 0, 0, 0, 0, 0, 0, 0, 0},
                  {0, 4, 0, 0, 0, 0, 0, 3, 0},
                  {0, 0, 0, 0, 2, 0, 0, 0, 0},
                  {6, 0, 0, 0, 0, 0, 3, 0, 0},
                  {0, 0, 0, 0, 0, 7, 0, 0, 0}};

    auto result = solve_diagonal_sudoku(input);
    if (0) { // debug
        std::println("Solved grid:");
        for (const auto& row : result) {
            std::println("{}", row);
        }
    }
    auto valid = is_valid_diagonal_sudoku(result);
    if (std::get<3>(valid) != Validity::Valid) {
        auto [row, col, num, reason] = valid;
        std::println("Invalid solution: {} at ({}, {}) - reason: {}", num, row,
                     col, static_cast<unsigned>(reason));
    }
    EXPECT_TRUE(std::get<3>(valid) == Validity::Valid);
    // Check clues preserved
    EXPECT_EQ(result[0][3], 6);
    EXPECT_EQ(result[1][2], 2);
    EXPECT_EQ(result[7][0], 6);
    EXPECT_EQ(result[8][5], 7);
    
    // Also test iterative DFS variant
    auto result_dfs = diagonal_sudoku_dfs::solve(input);
    auto valid_dfs = is_valid_diagonal_sudoku(result_dfs);
    EXPECT_TRUE(std::get<3>(valid_dfs) == Validity::Valid);
}

// clang-format on
