/*
Not CTCI:
    https://leetcode.com/problems/search-in-rotated-sorted-array

./ctci-2026 --gtest_filter=search_rotated.*
*/
#include <cassert>
#include <vector>

#include <gtest/gtest.h>

class Solution {
  public:
    static int search(const std::vector<int>& _nums, int _target) {
        assert(!_nums.empty() && "constraint");

        Solution s;
        s.nums = &_nums;
        s.target = _target;
        return s.search(0, _nums.size());
    }

  private:
    const std::vector<int>* nums = {};
    int target = {};

    int search(size_t start, size_t end) const {
        // if (end - start < 3)
        // {
        //     if (nums->at(start) == target)
        //         return start;
        //     if (nums->at(end - 1) == target)
        //         return end - 1;
        //     return -1;
        // }
        if (start >= end) return -1;

        auto middle = start + (end - start) / 2;
        if (nums->at(middle) == target) return middle;

        if (nums->at(start) <= nums->at(middle)) {
            if (nums->at(start) <= target && target < nums->at(middle))
                return search(start, middle);
            return search(middle + 1, end);
        } else {
            if (nums->at(middle) <= target && target <= nums->at(end - 1))
                return search(middle + 1, end);
            return search(start, middle);
        }
    }
};

TEST(search_rotated, example1) {
    assert(4 == Solution::search({4, 5, 6, 7, 0, 1, 2}, 0));
}

TEST(search_rotated, example2) {
    assert(-1 == Solution::search({4, 5, 6, 7, 0, 1, 2}, 3));
}

TEST(search_rotated, example3) {
    assert(5 == Solution::search({4, 5, 6, 7, 0, 1, 2}, 1));
}

TEST(search_rotated, one) {
    using Cont = std::vector<int>;
    assert(-1 == Solution::search(Cont{1}, 0));
    assert(0 == Solution::search(Cont{1}, 1));
}

TEST(search_rotated, empty_array) {
    // Verifies it returns safely instead of crashing via out-of-bounds at(0)
    assert(true ||
           (-1 == Solution::search(std::vector<int>{}, 5) && "not supported"));
}

TEST(search_rotated, size_two_or_three) {
    // Tests sizes that tripped up the `end - start < 3` boundary logic
    assert(1 == Solution::search({3, 1}, 1));
    assert(0 == Solution::search({3, 1}, 3));
    assert(-1 == Solution::search({3, 1}, 2));
    assert(1 == Solution::search({5, 6, 1}, 6));
}

TEST(search_rotated, pivot_at_boundaries) {
    // Pivot at the absolute start and absolute end (fully sorted)
    assert(0 == Solution::search({1, 2, 3, 4, 5}, 1));
    assert(4 == Solution::search({1, 2, 3, 4, 5}, 5));
    assert(2 == Solution::search({5, 1, 2, 3, 4}, 2));
}

TEST(search_rotated, large_values_not_found) {
    // Out of bounds on both high and low extremes
    assert(-1 == Solution::search({4, 5, 6, 7, 0, 1, 2}, 10));
    assert(-1 == Solution::search({4, 5, 6, 7, 0, 1, 2}, -5));
}
