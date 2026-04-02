"""
https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/maximum-non-overlapping-intervals

#greedy
"""

import unittest


def maximize_non_overlapping_meetings(meetings):
    """
    Find the maximum number of non-overlapping meetings that can be scheduled.

    Idea: Finishing an interval as early as possible leaves the maximum amount
    of "room" for subsequent intervals.
    """
    if not meetings:
        return 0

    # Sort meetings by their end times
    meetings.sort(key=lambda x: x[1])

    last_end_time = meetings[0][1]  # End time of the first meeting
    count = 1  # Count the first meeting

    for start, end in meetings:
        if start >= last_end_time:
            count += 1
            last_end_time = end

    return count


class TestMaximizeNonOverlappingMeetings(unittest.TestCase):
    """Unit tests for maximize_non_overlapping_meetings."""

    def test_empty_meetings(self):
        """Empty meeting list returns zero."""
        self.assertEqual(maximize_non_overlapping_meetings([]), 0)

    def test_single_meeting(self):
        """Single meeting is always selectable."""
        self.assertEqual(maximize_non_overlapping_meetings([[1, 2]]), 1)

    def test_non_overlapping_meetings(self):
        """All non-overlapping meetings are counted."""
        meetings = [[1, 2], [2, 3], [3, 4]]
        self.assertEqual(maximize_non_overlapping_meetings(meetings), 3)

    def test_overlapping_meetings(self):
        """Choose the maximum number of non-overlapping meetings."""
        meetings = [[1, 5], [2, 3], [3, 4], [4, 6]]
        self.assertEqual(maximize_non_overlapping_meetings(meetings), 3)

        meetings = [[1, 2], [2, 3], [3, 4], [1, 3]]
        self.assertEqual(maximize_non_overlapping_meetings(meetings), 3)

        meetings = [[0, 5], [0, 1], [1, 2], [2, 3], [3, 5], [4, 6]]
        self.assertEqual(maximize_non_overlapping_meetings(meetings), 4)

    def test_unsorted_input(self):
        """Function handles unsorted meeting lists."""
        meetings = [[5, 7], [1, 3], [2, 4], [3, 5]]
        self.assertEqual(maximize_non_overlapping_meetings(meetings), 3)


if __name__ == "__main__":
    unittest.main()
