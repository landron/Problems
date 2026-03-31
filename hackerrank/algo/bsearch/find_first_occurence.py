"""
Find the first occurrence of a target value in a sorted array.
https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/first-occurrence-in-event-code-log
"""

import bisect
import unittest


def find_first_occurrence(arr, target):
    """find the first occurrence of target in arr, or -1 if not found"""
    index = bisect.bisect_left(arr, target)
    if index < len(arr) and arr[index] == target:
        return index
    return -1


class TestFindFirstOccurrence(unittest.TestCase):
    """unit tests for find_first_occurrence"""

    def test_empty_list(self):
        """test empty list"""
        self.assertEqual(find_first_occurrence([], 1), -1)

    def test_single_element_not_found(self):
        """test single element not found"""
        self.assertEqual(find_first_occurrence([1], 2), -1)

    def test_single_element_found(self):
        """test single element found"""
        self.assertEqual(find_first_occurrence([1], 1), 0)

    def test_sample_cases(self):
        """test sample cases"""
        self.assertEqual(find_first_occurrence([1, 2, 3, 4, 5], 4), 3)
        self.assertEqual(find_first_occurrence([1, 2, 3, 4, 4, 5], 4), 3)
        self.assertEqual(find_first_occurrence([1, 2, 3, 3, 4, 4, 5], 3), 2)


def debug_validations():
    """unit testing"""
    unittest.main()


def main():
    """main"""
    debug_validations()


if __name__ == "__main__":
    main()
