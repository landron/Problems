#include <vector>
#include <span>

#include <gtest/gtest.h>

template <std::ranges::random_access_range R>
// Only allows vectors, arrays, and spans
int findFirstOccurrence(const R& nums, int target) {
    const auto found = std::lower_bound(std::begin(nums), std::end(nums), target);
    if (found == std::end(nums) || *found != target)
        return -1;
    return std::distance(std::begin(nums), found);
}

int findFirstOccurrence_Vector(const std::vector<int>& nums, int target) {
    const auto found = std::lower_bound(nums.begin(), nums.end(), target);
    if (found == nums.end() || *found != target)    
        return -1;
    return std::distance(nums.begin(), found);
}

int findFirstOccurrence_Manual(const std::vector<int>& nums, int target) {
    if (nums.empty())
        return -1;
    
    auto found = -1;
    size_t left = 0, right = nums.size() - 1;
    for (; left <= right;) {
        const auto mid = left + (right-left)/2;
        if (mid == left || mid == right) {
            if (nums[mid] == target)
                found = mid;
            break;
        }
        if (nums[mid] < target) {
            left = mid;
        } else {
            if (nums[mid] == target)
                found = mid;
            right = mid;
        }
    }
    return found;
}

int findFirstOccurrence_Timeout(const std::vector<int>& nums, int target) {
    switch (nums.size()) {
        case 0: return -1;
        case 1: return nums[0] == target ? 0 : -1;
    }
    
    auto mid = nums.size()/2;
    for (;mid && mid < nums.size() && nums[mid] != target;) {
        if (nums[mid] < target) {
            auto mid2 = (nums.size() - mid)/2;
            if (mid2 == 0)
                mid2 = 1;
            mid = mid + mid2;
        } else {
            mid /= 2;
        }
    }
    if ((mid >= nums.size()) || nums[mid] != target)
        return -1;
    for (;mid > 0 && nums[mid] == target;--mid); // ! TIMEOUT test 12
    return nums[mid] == target ? mid : mid+1;
}

TEST(test_limits, empty_list) {
    EXPECT_EQ(findFirstOccurrence_Vector({}, 1), -1);
    EXPECT_EQ(findFirstOccurrence_Manual({}, 1), -1);
    EXPECT_EQ(findFirstOccurrence_Timeout({}, 1), -1);
}

TEST(test_limits, single_element_not_found) {
    EXPECT_EQ(findFirstOccurrence_Vector({1}, 2), -1);
    EXPECT_EQ(findFirstOccurrence_Manual({1}, 2), -1);
    EXPECT_EQ(findFirstOccurrence_Timeout({1}, 2), -1);
}

TEST(test_limits, single_element_found) {
    EXPECT_EQ(findFirstOccurrence_Vector({1}, 1), 0);
    EXPECT_EQ(findFirstOccurrence_Manual({1}, 1), 0);
    EXPECT_EQ(findFirstOccurrence_Timeout({1}, 1), 0);
}

TEST(test_sample, test1) {
    EXPECT_EQ(findFirstOccurrence_Vector({1, 2, 3, 4, 5}, 4), 3);
    EXPECT_EQ(findFirstOccurrence_Manual({1, 2, 3, 4, 5}, 4), 3);
    EXPECT_EQ(findFirstOccurrence_Timeout({1, 2, 3, 4, 5}, 4), 3);
    EXPECT_EQ(findFirstOccurrence_Vector({1, 2, 3, 4, 4, 5}, 4), 3);
    EXPECT_EQ(findFirstOccurrence_Manual({1, 2, 3, 4, 4, 5}, 4), 3);
    EXPECT_EQ(findFirstOccurrence_Timeout({1, 2, 3, 4, 4, 5}, 4), 3);
    EXPECT_EQ(findFirstOccurrence_Vector({1, 2, 3, 3, 4, 4, 5}, 3), 2);
    EXPECT_EQ(findFirstOccurrence_Manual({1, 2, 3, 3, 4, 4, 5}, 3), 2);
    EXPECT_EQ(findFirstOccurrence_Timeout({1, 2, 3, 3, 4, 4, 5}, 3), 2);
}

TEST(test_ranges, array_and_span) {
    const int arr[] = {1, 2, 3, 4, 4, 5};
    EXPECT_EQ(findFirstOccurrence(arr, 4), 3);

    // const span not necessary
    /*const*/ std::span<const int> sp(arr);
    EXPECT_EQ(findFirstOccurrence(sp, 4), 3);
}
