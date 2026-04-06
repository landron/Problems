"""
N-Queens problem: place N non-attacking queens on an NxN board.
https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/shortest-path-with-processing-delays/

Complexity: O(N!) Time | O(N) Space
Tags: #backtracking #recursion #dynamic-programming
ruff & pylint clean.

Time Complexity: O(N!)
======================
* see is_safe() for some optimizations that can make the algorithm much faster in practice,
but the worst-case complexity remains O(N!) due to the nature of backtracking.
* For large values of N (typically N>100), standard backtracking is computationally
infeasible due to its O(N!) worst-case complexity. In these cases,
Conflict-Repair (Heuristic Search) or Constraint Satisfaction algorithms are more effective.
"""

import unittest


def solve_n_queens(grid):
    """
    Solves N-Queens problem: place N non-attacking queens on an NxN board.

    Args:
        grid: NxN matrix where 1 represents obstacles, 0 represents empty cells

    Returns:
        True if a valid placement exists, False otherwise

    Time Complexity: O(N!) - worst case explores all permutations via backtracking
        The N-Queens algorithm uses backtracking which explores queen placements recursively:
            First queen: N possible positions
            Second queen: ~(N-1) valid positions (excluding conflicts)
            Third queen: ~(N-2) valid positions
            ...and so on
        This gives us N x (N-1) x (N-2) x ... x 1 = N! combinations in the worst case.
        Note: The caching optimization makes is_safe() O(1) instead of O(N), drastically
        improving real-world performance, but doesn't reduce the exponential O(N!) bound
        since the backtracking still explores exponential decision tree.
    Space Complexity: O(N) - for solution array storage + 3 cached sets (if optimized)
    """
    n = len(grid)
    solution = [-1] * n  # solution[row] = col where queen is placed in that row

    def is_safe(row, col):
        """Check if placing a queen at (row, col) is safe."""
        # Check if cell is blocked
        if grid[row][col] == 1:
            return False

        # Check column and diagonals above current row
        # OPTIMIZATION OPPORTUNITY 1: Cache occupied columns and diagonals in sets
        # (occupied_cols, diag1=row-col, diag2=row+col) to make is_safe() O(1).
        # Trade-off: +O(N) space but massive speedup for each check.
        #
        # OPTIMIZATION OPPORTUNITY 2: Bitmasking - use 3 integers with bit flags instead
        # of sets. Each bit represents if col/diagonal is occupied. col_mask, diag1_mask,
        # diag2_mask. Check becomes bitwise AND: "col_mask & (1 << col)". Even faster!
        for r in range(row):
            if solution[r] == col:  # Same column
                return False
            if abs(solution[r] - col) == abs(r - row):  # Diagonal
                return False
        return True

    row = 0
    while 0 <= row < n:
        start_col = solution[row] + 1 if solution[row] != -1 else 0

        # Reset current row before trying next column
        solution[row] = -1

        found = False
        for col in range(start_col, n):
            if is_safe(row, col):
                solution[row] = col
                row += 1
                found = True
                break

        if not found:
            row -= 1  # Backtrack

    return row == n


class TestSolveNQueens(unittest.TestCase):
    """Unit tests for the N-Queens solver."""

    def test_3x3_no_solution(self):
        """3x3 grid with no solution."""
        self.assertFalse(solve_n_queens([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))

    def test_4x4_empty_grid(self):
        """4x4 empty grid has a solution."""
        self.assertTrue(
            solve_n_queens([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        )

    def test_4x4_corners_blocked(self):
        """4x4 grid with opposite corners blocked."""
        self.assertTrue(
            solve_n_queens([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])
        )

    def test_4x4_diagonal_blocked(self):
        """4x4 grid with main diagonal blocked."""
        self.assertTrue(
            solve_n_queens([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        )

    def test_4x4_mixed_obstacles(self):
        """4x4 grid with mixed obstacles."""
        self.assertTrue(
            solve_n_queens([[1, 0, 0, 1], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]])
        )

    def test_4x4_sparse_obstacles(self):
        """4x4 grid with sparse obstacles."""
        self.assertTrue(
            solve_n_queens([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]])
        )

    def test_4x4_row_blocked(self):
        """4x4 grid with entire row blocked."""
        self.assertFalse(
            solve_n_queens([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1]])
        )

    def test_4x4_column_threat(self):
        """4x4 grid with obstacles creating column threats."""
        self.assertTrue(
            solve_n_queens([[1, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]])
        )

    def test_4x4_column_blocked(self):
        """4x4 grid with entire column blocked."""
        self.assertFalse(
            solve_n_queens([[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]])
        )


if __name__ == "__main__":
    unittest.main()
