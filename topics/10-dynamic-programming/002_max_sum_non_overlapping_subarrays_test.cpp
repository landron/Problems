/*
./topics --gtest_filter=MaxSumNonOverlappingSubarrays.TimeoutTest
./topics --gtest_filter=MaxSumNonOverlappingSubarrays.*
*/
#include <gtest/gtest.h>

#include "002_max_sum_non_overlapping_subarrays.h"

template <typename T>
void runMinimalTest() {
    EXPECT_EQ(7, T().maximumSum({4, 1, -5, 2}, 2, 1, 3));
    EXPECT_EQ(8, T().maximumSum({1, 0, 3, 4}, 2, 1, 2));
    EXPECT_EQ(6, T().maximumSum({-1, 7, -4}, 1, 2, 3));
    EXPECT_EQ(-1, T().maximumSum({-3, -4, -1}, 2, 1, 2));
}

TEST(MaxSumNonOverlappingSubarrays, Minimal) {
    runMinimalTest<SolutionDP>();
    runMinimalTest<SolutionPrecalculatedSubarrays>();
}

TEST(MaxSumNonOverlappingSubarrays, TimeoutTest) {
    std::vector<int> nums(1000, 1);
    EXPECT_EQ(1000,
              SolutionPrecalculatedSubarrays().maximumSum(nums, 1000, 1, 1000));
}
