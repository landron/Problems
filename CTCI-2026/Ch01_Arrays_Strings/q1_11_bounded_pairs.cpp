/*
https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/count-number-pairs

the provided array is already sorted.
*/
#include <vector>
#include <algorithm>
#include <iostream>

#include "gtest/gtest.h"

// https://gemini.google.com version
int countBoundedPairs(const std::vector<int>& prices, int budget) {
    if (prices.size() < 2) return 0;

    std::size_t count = 0;
    auto left = prices.begin();
    auto right = std::prev(prices.end());

    while (left < right) {
        if (*left + *right <= budget) {
            // If (left + right) works, then left + every element 
            // between left and right also works.
            count += std::distance(left, right);
            ++left; 
        } else {
            // Sum too high, make the right side smaller
            --right;
        }
    }
    return static_cast<int>(count);
}

// O(N): two pointer technique
int countBoundedPairs_2(const std::vector<int>& prices, int budget) {
    if (prices.empty()) return 0;
    
    auto count = std::size_t{0};
    auto end = std::prev(prices.end());
    for (auto begin = prices.begin(); begin != end; ++begin) {
        for (;end != begin;--end)
            if (*end + *begin <= budget) break;
        if (end == begin) break;
        //auto step = std::distance(begin, end);
        //std::cout << "distance: " << step << std::endl;
        //count += step;
        count += std::distance(begin, end);
    }
    return static_cast<int>(count);
}

// O(N*logN)
int countBoundedPairs_1(const std::vector<int>& prices, int budget) {
    auto end = std::upper_bound(prices.begin(), prices.end(), budget);
    auto count = std::size_t{0};
    for (auto i = prices.begin(); i != end; ++i) {
        auto begin = i;
        begin++;
        auto endi = std::upper_bound(begin, end, budget - *i);
        count += std::distance(begin, endi);
    }
    return count;
}

static void expect_bounded_pairs(
    const std::vector<int>& prices,
    int budget,
    int expected)
{
    EXPECT_EQ(countBoundedPairs_1(prices, budget), expected);
    EXPECT_EQ(countBoundedPairs_2(prices, budget), expected);
    EXPECT_EQ(countBoundedPairs(prices, budget), expected);
}

TEST(CountBoundedPairs, EmptyPrices) {
    expect_bounded_pairs({}, 10, 0);
}

TEST(CountBoundedPairs, SinglePrice) {
    expect_bounded_pairs({5}, 10, 0);
}

TEST(CountBoundedPairs, NoValidPairs) {
    expect_bounded_pairs({2, 3, 5, 8}, 4, 0);
}

TEST(CountBoundedPairs, SomeValidPairs) {
    expect_bounded_pairs({1, 2, 3}, 7, 3);

    expect_bounded_pairs({1, 2, 3, 4, 5}, 5, 4);
    expect_bounded_pairs({1, 2, 3, 4, 5}, 6, 6);
    expect_bounded_pairs({1, 2, 3, 4, 5}, 7, 8);
}

TEST(CountBoundedPairs, AllPairsValid) {
    expect_bounded_pairs({1, 1, 1, 1}, 2, 6);
}

TEST(CountBoundedPairs, LargeBudgetAllPairs) {
    expect_bounded_pairs({2, 4, 6, 8}, 100, 6);
}

// https://gemini.google.com
TEST(CountBoundedPairs, StandardCases) {
    // Basic overlap
    expect_bounded_pairs({1, 2, 3, 4, 5}, 6, 6); 
    // Pairs: (1,2), (1,3), (1,4), (1,5), (2,3), (2,4)
    
    // Nothing fits
    expect_bounded_pairs({10, 20, 30}, 5, 0);
    
    // Everything fits
    expect_bounded_pairs({1, 2, 3}, 10, 3);
}

// https://gemini.google.com
TEST(CountBoundedPairs, BoundaryConditions) {
    // Minimal size
    expect_bounded_pairs({}, 10, 0);
    expect_bounded_pairs({5}, 10, 0);
    expect_bounded_pairs({5, 5}, 10, 1);
    
    // Large values
    expect_bounded_pairs({1, 100, 100, 100}, 101, 3);
}

