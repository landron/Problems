"""Find the first strictly greater element following each position in an array.

https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/next-greater-element-with-offset

Complexity: O(N) Time | O(N) Space
Tags: #stack #monotonic-stack
Compliance: black, pylint, ruff
    ruff check Ch04_Stacks_and_Queues/stack_monotonic_next_greater.py
"""

from collections import deque
from typing import List, Tuple
import unittest

# Type alias for clarity
Result = List[Tuple[int, int]]  # List of (next_greater_value, distance) tuples


def find_next_greater_elements_gemini(readings: List[int]) -> Result:
    """
    Find next greater element and distance for each element (Gemini variant).

    Args:
        readings: List of integers representing values to process.

    Returns:
        List of (next_greater_value, distance) tuples. (-1, -1) if no greater element.

    Approach: Monotonic Stack (strictly increasing)
        A stack is "monotonic" if its elements are always in a specific order.

    Time Complexity: O(N) amortized - Each element pushed/popped exactly once
        Nested while loop doesn't escalate to O(N²) because each element pops at most once.
    Space Complexity: O(N) - Stack and result array storage
    """
    if not readings:
        return []

    n = len(readings)
    result = [(-1, -1)] * n
    stack = []  # Stores (value, index)

    # Iterate backwards
    for i in range(n - 1, -1, -1):
        current_val = readings[i]

        # 1. Pop elements that are smaller or equal (they can't be "Greater")
        while stack and stack[-1][0] <= current_val:
            stack.pop()

        # 2. If stack isn't empty, the top is our Next Greater Element
        if stack:
            greater_val, greater_idx = stack[-1]
            result[i] = (greater_val, greater_idx - i)

        # 3. Push current element as a candidate for those to the left
        stack.append((current_val, i))

    return result


def find_next_greater_elements_mine(readings: List[int]) -> Result:
    """
    Find next greater element and distance for each element (Custom variant).

    Args:
        readings: List of integers representing values to process.

    Returns:
        List of (next_greater_value, distance) tuples. (-1, -1) if no greater element.

    Approach: Monotonic Stack with deque for left-insertion efficiency.

    Time Complexity: O(N) amortized - Each element processed once
        Inner while loop pops each element at most once total.
    Space Complexity: O(N) - Stack and deque storage (deque→list conversion adds temp memory)
    """
    if not readings:
        return []

    def add(stack: List[Tuple[int, int]], value: int, index: int) -> None:
        """Maintain monotonic stack invariant by popping smaller/equal elements."""
        while stack and value >= stack[-1][0]:
            stack.pop()
        stack.append((value, index))

    stack = [(readings[-1], len(readings) - 1)]
    result = deque([(-1, -1)])
    for i in range(len(readings) - 2, -1, -1):
        val = readings[i]
        if stack[-1][0] != val:
            add(stack, val, i)
            if len(stack) == 1:
                result.appendleft((-1, -1))
            else:
                greater = stack[-2]
                result.appendleft((greater[0], greater[1] - i))
        else:
            greater = result[0]
            if greater[1] > 0:
                greater = (greater[0], greater[1] + 1)
            result.appendleft(greater)

    # Convert deque to list - O(N) operation but necessary for return type consistency
    return list(result)


class TestNextGreaterElements(unittest.TestCase):
    """Unit tests for next greater element functions."""

    def _test_both_implementations(
        self, test_input: List[int], expected: Result
    ) -> None:
        """Helper method to test both implementations against expected output.

        Args:
            test_input: Input array for testing.
            expected: Expected output from both implementations.
        """
        result_gemini = find_next_greater_elements_gemini(test_input)
        result_mine = find_next_greater_elements_mine(test_input)
        self.assertEqual(result_gemini, expected, f"Gemini failed for {test_input}")
        self.assertEqual(result_mine, expected, f"Mine failed for {test_input}")

    def test_basic_case(self):
        """Test basic case: [2, 1, 2, 4, 3]."""
        self._test_both_implementations(
            [2, 1, 2, 4, 3], [(4, 3), (2, 1), (4, 1), (-1, -1), (-1, -1)]
        )

    def test_sorted_ascending(self):
        """Test sorted ascending array - every element has a next greater."""
        self._test_both_implementations(
            [1, 2, 3, 4, 5], [(2, 1), (3, 1), (4, 1), (5, 1), (-1, -1)]
        )

    def test_sorted_descending(self):
        """Test sorted descending array - no next greater elements exist."""
        self._test_both_implementations(
            [5, 4, 3, 2, 1], [(-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1)]
        )

    def test_single_element(self):
        """Test single element array."""
        self._test_both_implementations([42], [(-1, -1)])

    def test_empty_array(self):
        """Test empty array."""
        self._test_both_implementations([], [])

    def test_duplicates(self):
        """Test array with duplicate elements."""
        result_gemini = find_next_greater_elements_gemini([3, 3, 3])
        result_mine = find_next_greater_elements_mine([3, 3, 3])
        self.assertTrue(
            all(r[0] == -1 for r in result_gemini),
            "Gemini: all elements equal should have no next greater",
        )
        self.assertTrue(
            all(r[0] == -1 for r in result_mine),
            "Mine: all elements equal should have no next greater",
        )

    def test_two_elements(self):
        """Test two element array."""
        self._test_both_implementations([1, 5], [(5, 1), (-1, -1)])

    def test_saw_pattern(self):
        """Test alternating high-low pattern."""
        test_input = [1, 5, 2, 4, 3]
        expected = [(5, 1), (-1, -1), (4, 1), (-1, -1), (-1, -1)]
        self._test_both_implementations(test_input, expected)

    def test_large_values(self):
        """Test with large numbers."""
        test_input = [1000, 500, 750, 800]
        expected = [(-1, -1), (750, 1), (800, 1), (-1, -1)]
        self._test_both_implementations(test_input, expected)


if __name__ == "__main__":
    unittest.main()
