#include "gtest/gtest.h"

#include "../common/linked_list_utils.hpp"

Node* kth_to_last(Node* head, size_t k) {
    if (!head) return nullptr;

    auto distance = k;
    auto second = head;
    for (; second && distance; second = second->next.get(), --distance) {
        // Empty body is clearer than a trailing semicolon
    }
    if (!second) {
        if (distance == 0) {
            // k is exactly the length of the list, so we return the head
            return head;
        }
        return nullptr;
    }
    auto first = head;
    for (; second; first = first->next.get(), second = second->next.get()) {
        // Empty body is clearer than a trailing semicolon
    }
    return first;
}

TEST(test_limits, k_greater_than_length) {
    auto list = create_linked_list({1, 2, 3});
    auto node = kth_to_last(list.get(), 4); // k is larger than the list
    EXPECT_EQ(node, nullptr); // Or however you chose to handle errors
}

TEST(test_limits, empty_list) {
    std::unique_ptr<Node> list;
    auto node = kth_to_last(list.get(), 1);
    EXPECT_EQ(node, nullptr);
}

TEST(test_limits, single_node) {
    auto list = create_linked_list({55});
    auto node = kth_to_last(list.get(), 1);
    ASSERT_NE(node, nullptr);
    EXPECT_EQ(node->data, 55);
}

TEST(test_limits, boundaries) {
    auto list = create_linked_list({10, 20, 30, 40});
    
    // k = 1: The tail
    auto tail = kth_to_last(list.get(), 1);
    EXPECT_EQ(tail->data, 40);
    
    // k = length: The head
    auto head = kth_to_last(list.get(), 4);
    EXPECT_EQ(head->data, 10);
}

TEST(test_sample, test1) {
    auto list = create_linked_list({1, 2, 3, 4, 5});
    auto node = kth_to_last(list.get(), 2);
    ASSERT_TRUE(node);
    EXPECT_EQ(node->data, 4);
}
