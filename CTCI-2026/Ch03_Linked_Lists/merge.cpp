/*
Not CTCI:
    https://leetcode.com/problems/merge-two-sorted-lists/

./ctci-2026 --gtest_filter=merge_lists.*
*/
#include <memory>

#include <gtest/gtest.h>

#include "../common/linked_list_utils.hpp"

class Solution {
  public:
    using ListNode = RawNode<int>;
    using UniqueList = UniqueRawList<int>;

  public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        if (!list1) return list2;
        if (!list2) return list1;

        auto mprev_sp = std::make_unique<ListNode>();
        auto mprev = mprev_sp.get();
        while (list1 && list2) {
            if (list1->val < list2->val) {
                mprev->next = list1;
                list1 = list1->next;
            } else {
                mprev->next = list2;
                list2 = list2->next;
            }
            mprev = mprev->next;
            mprev->next = nullptr;
        }
        while (list1) {
            mprev->next = list1;
            list1 = list1->next;
            mprev = mprev->next;
            mprev->next = nullptr;
        }
        while (list2) {
            mprev->next = list2;
            list2 = list2->next;
            mprev = mprev->next;
            mprev->next = nullptr;
        }
        return mprev_sp->next;
    }
};

TEST(merge_lists, example1) {
    auto list1 = create_linked_list_raw({1, 2, 4});
    auto list2 = create_linked_list_raw({1, 3, 4});
    auto merged = Solution::UniqueList(
        Solution().mergeTwoLists(list1.release(), list2.release()));
    auto merged_V = to_vector(merged.get());
    assert((merged_V == std::vector<int>{1, 1, 2, 3, 4, 4}));
}

TEST(merge_lists, both_empty) {
    auto list1 = create_linked_list_raw<int>({});
    auto list2 = create_linked_list_raw<int>({});
    auto merged = Solution::UniqueList(
        Solution().mergeTwoLists(list1.release(), list2.release()));
    auto merged_V = to_vector(merged.get());
    assert((merged_V == std::vector<int>{}));
}

TEST(merge_lists, one_empty) {
    auto list1 = create_linked_list_raw<int>({0});
    auto list2 = create_linked_list_raw<int>({});
    auto merged = Solution::UniqueList(
        Solution().mergeTwoLists(list1.release(), list2.release()));
    auto merged_V = to_vector(merged.get());
    assert((merged_V == std::vector<int>{0}));
}

TEST(merge_lists, one_node_each) {
    auto list1 = create_linked_list_raw({2});
    auto list2 = create_linked_list_raw({1});
    auto merged = UniqueRawList<int>(
        Solution().mergeTwoLists(list1.release(), list2.release()));
    auto merged_V = to_vector(merged.get());
    assert((merged_V == std::vector<int>{1, 2}));
}

TEST(merge_lists, uneven_lengths) {
    auto list1 = create_linked_list_raw({1, 5, 9});
    auto list2 = create_linked_list_raw({2});
    auto merged = UniqueRawList<int>(
        Solution().mergeTwoLists(list1.release(), list2.release()));
    auto merged_V = to_vector(merged.get());
    assert((merged_V == std::vector<int>{1, 2, 5, 9}));
}

TEST(merge_lists, duplicate_streaks) {
    auto list1 = create_linked_list_raw({1, 1, 1});
    auto list2 = create_linked_list_raw({1, 1});
    auto merged = UniqueRawList<int>(
        Solution().mergeTwoLists(list1.release(), list2.release()));
    auto merged_V = to_vector(merged.get());
    assert((merged_V == std::vector<int>{1, 1, 1, 1, 1}));
}

TEST(merge_lists, negative_values) {
    auto list1 = create_linked_list_raw({-10, -5, 0});
    auto list2 = create_linked_list_raw({-7, 2});
    auto merged = UniqueRawList<int>(
        Solution().mergeTwoLists(list1.release(), list2.release()));
    auto merged_V = to_vector(merged.get());
    assert((merged_V == std::vector<int>{-10, -7, -5, 0, 2}));
}
