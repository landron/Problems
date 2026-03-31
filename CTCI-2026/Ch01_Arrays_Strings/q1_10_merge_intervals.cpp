/* 
Constraints:
    Intervals are not necessarily sorted by start time.
    Time complexity goal: O(nlogn).
    Space complexity goal: O(n) (for the output).
*/
#include "gtest/gtest.h"
#include <algorithm>
#include <vector>

using Interval = std::pair<size_t, size_t>;
using Intervals = std::vector<Interval>;

Intervals merge_intervals_1(Intervals& intervals) {
    if (intervals.empty())
        return {};

    std::sort(intervals.begin(), intervals.end(), [](const auto& a, const auto& b) {
        if (a.first == b.first) {
            return a.second < b.second;
        }
        return a.first < b.first;
    });

    Intervals merged;
    auto current = intervals.begin();
    while (current != intervals.end()) {
        auto next = *current;
        for (; current != intervals.end(); ++current) {
            if (current->first > next.second) {
                break;
            }
            next.second = std::max(next.second, current->second);
        }
        merged.push_back(next);
    }
    return merged;
}

// Intervals merge_intervals_1(Intervals& intervals) {
// }

TEST(test_merge_intervals, sample_overlapping_intervals) {
    Intervals intervals{{1, 3}, {2, 6}, {8, 10}, {15, 18}};
    Intervals expected{{1, 6}, {8, 10}, {15, 18}};

    EXPECT_EQ(merge_intervals_1(intervals), expected);
}

TEST(test_merge_intervals, unsorted_input) {
    Intervals intervals{{5, 6}, {1, 4}, {2, 3}, {8, 10}};
    Intervals expected{{1, 4}, {5, 6}, {8, 10}};

    EXPECT_EQ(merge_intervals_1(intervals), expected);
}

TEST(test_merge_intervals, no_overlaps) {
    Intervals intervals{{1, 2}, {3, 4}, {5, 6}};
    Intervals expected{{1, 2}, {3, 4}, {5, 6}};

    EXPECT_EQ(merge_intervals_1(intervals), expected);
}

TEST(test_merge_intervals, nested_and_same_start) {
    Intervals intervals{{1, 4}, {1, 5}, {2, 3}, {6, 8}};
    Intervals expected{{1, 5}, {6, 8}};

    EXPECT_EQ(merge_intervals_1(intervals), expected);
}

TEST(test_merge_intervals, empty_list) {
    Intervals intervals;
    Intervals expected;

    EXPECT_EQ(merge_intervals_1(intervals), expected);
}
