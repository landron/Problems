/*
Constraints:
    Intervals are not necessarily sorted by start time.
    Time complexity goal: O(nlogn).
    Space complexity goal: O(n) (for the output).
*/
#include <algorithm>
#include <ranges>
#include <vector>

#include <gtest/gtest.h>

// https://gemini.google.com version
template <std::ranges::random_access_range R>
auto merge_intervals(R& intervals)
    -> std::vector<std::ranges::range_value_t<R>> {
    using Interval = std::ranges::range_value_t<R>;

    if (std::ranges::empty(intervals)) return {};

    // 1. Sort in-place (O(n log n))
    std::ranges::sort(intervals);

    // 2. Single-pass merge (O(n))
    std::vector<Interval> merged;
    merged.reserve(intervals.size()); // Optimization: avoid reallocations

    merged.push_back(intervals[0]);

    for (const auto& current : intervals | std::views::drop(1)) {
        auto& last = merged.back();

        if (current.first <= last.second) {
            // There is an overlap, extend the boundary
            last.second = std::max(last.second, current.second);
        } else {
            // No overlap, start a new interval
            merged.push_back(current);
        }
    }

    return merged;
}

// also see merge_intervals_2 comment
template <std::ranges::random_access_range R>
auto merge_intervals_3(R& intervals)
    -> std::vector<std::ranges::range_value_t<R>> {
    if (std::ranges::empty(intervals)) return {};

    // std::pair already has an operator< that performs exactly that
    // "lexicographical" comparison (compare first, then second).
    std::ranges::sort(intervals);

    auto merger = [](const R& intervals) {
        std::vector<std::ranges::range_value_t<R>> merged;
        merged.reserve(std::ranges::size(intervals));

        auto current = std::ranges::begin(intervals);
        while (current != std::ranges::cend(intervals)) {
            auto next = *current;
            for (; current != std::ranges::cend(intervals); ++current) {
                if (current->first > next.second) {
                    break;
                }
                next.second = std::max(next.second, current->second);
            }
            merged.push_back(next);
        }
        return merged;
    };
    return merger(intervals);
}

template <std::ranges::random_access_range R>
// Here, using auto ... -> is a stylistic choice that signals: "I am writing
// modern, template-heavy C++."
auto merge_intervals_2(R& intervals)
    -> std::vector<std::ranges::range_value_t<R>> {
    if (std::ranges::empty(intervals)) return {};

    // Since C++17, lambdas are implicitly constexpr if they satisfy the
    // requirements (i.e., they don't do anything illegal in a constant
    // expression).
    std::ranges::sort(intervals, [](auto const& a, auto const& b) constexpr {
        return a.first < b.first || (a.first == b.first && a.second < b.second);
    });

    using value_type = std::ranges::range_value_t<R>;
    std::vector<value_type> merged;
    auto current = std::ranges::begin(intervals);
    auto const end = std::ranges::end(intervals);
    while (current != end) {
        auto next = *current;
        for (; current != end; ++current) {
            if (current->first > next.second) {
                break;
            }
            next.second = std::max(next.second, current->second);
        }
        merged.push_back(next);
    }
    return merged;
}

// using Interval = std::pair<size_t, size_t>;
// using Intervals = std::vector<Interval>;
using Intervals = std::vector<std::pair<size_t, size_t>>;

Intervals merge_intervals_1(Intervals& intervals) {
    if (intervals.empty()) return {};

    std::sort(intervals.begin(), intervals.end(),
              [](const auto& a, const auto& b) {
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

TEST(test_merge_intervals, sample_overlapping_intervals) {
    const auto intervals = Intervals{{1, 3}, {2, 6}, {8, 10}, {15, 18}};
    const auto expected = Intervals{{1, 6}, {8, 10}, {15, 18}};

    auto run_test = [&](auto&& func) {
        auto copy = intervals;
        EXPECT_EQ(func(copy), expected);
    };

    run_test(merge_intervals_1);
    // Use a lambda to "anchor" the template call
    run_test([](auto& i) { return merge_intervals(i); });
    run_test([](auto& i) { return merge_intervals_2(i); });
    run_test([](auto& i) { return merge_intervals_3(i); });
}

TEST(test_merge_intervals, unsorted_input) {
    Intervals intervals{{5, 6}, {1, 4}, {2, 3}, {8, 10}};
    Intervals expected{{1, 4}, {5, 6}, {8, 10}};

    EXPECT_EQ(merge_intervals(intervals), expected);
    EXPECT_EQ(merge_intervals_1(intervals), expected);
    EXPECT_EQ(merge_intervals_2(intervals), expected);
    EXPECT_EQ(merge_intervals_3(intervals), expected);
}

TEST(test_merge_intervals, no_overlaps) {
    Intervals intervals{{1, 2}, {3, 4}, {5, 6}};
    Intervals expected{{1, 2}, {3, 4}, {5, 6}};

    EXPECT_EQ(merge_intervals(intervals), expected);
    EXPECT_EQ(merge_intervals_1(intervals), expected);
    EXPECT_EQ(merge_intervals_2(intervals), expected);
    EXPECT_EQ(merge_intervals_3(intervals), expected);
}

TEST(test_merge_intervals, nested_and_same_start) {
    Intervals intervals{{1, 4}, {1, 5}, {2, 3}, {6, 8}};
    Intervals expected{{1, 5}, {6, 8}};

    EXPECT_EQ(merge_intervals(intervals), expected);
    EXPECT_EQ(merge_intervals_1(intervals), expected);
    EXPECT_EQ(merge_intervals_2(intervals), expected);
    EXPECT_EQ(merge_intervals_3(intervals), expected);
}

TEST(test_merge_intervals, empty_list) {
    Intervals intervals;
    Intervals expected;

    EXPECT_EQ(merge_intervals(intervals), expected);
    EXPECT_EQ(merge_intervals_1(intervals), expected);
    EXPECT_EQ(merge_intervals_2(intervals), expected);
    EXPECT_EQ(merge_intervals_3(intervals), expected);
}
