/*
./ctci-2026 --gtest_filter=kth_to_last.*
*/
#include <gtest/gtest.h>

#include "../common/linked_list_utils.hpp"

/** Returns the kth to last node in a singly linked list.
 *
 * Single-pass two-pointer approach is optimal: O(n) time, O(1) extra space.
 */
template <typename NodePtr>
[[nodiscard]] NodePtr get_kth_to_last_impl(NodePtr head, size_t k) noexcept {
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

namespace kth_to_last {

using Node = ::Node<int>;

Node* get_kth_to_last(Node* head, size_t k) noexcept {
    return get_kth_to_last_impl(head, k);
}

const Node* get_kth_to_last(const Node* head, size_t k) noexcept {
    return get_kth_to_last_impl(head, k);
}

} // namespace kth_to_last

TEST(kth_to_last, k_greater_than_length) {
    auto list = create_linked_list({1, 2, 3});
    auto node = kth_to_last::get_kth_to_last(list.get(),
                                             4); // k is larger than the list
    EXPECT_EQ(node, nullptr); // Or however you chose to handle errors
}

TEST(kth_to_last, empty_list) {
    std::unique_ptr<kth_to_last::Node> list;
    auto node = kth_to_last::get_kth_to_last(list.get(), 1);
    EXPECT_EQ(node, nullptr);
}

TEST(kth_to_last, single_node) {
    auto list = create_linked_list({55});
    auto node = kth_to_last::get_kth_to_last(list.get(), 1);
    ASSERT_NE(node, nullptr);
    EXPECT_EQ((int)*node, 55);
}

TEST(kth_to_last, const_and_non_const) {
    auto list = create_linked_list({1, 2, 3, 4, 5});
    auto mutable_result = kth_to_last::get_kth_to_last(list.get(), 2);
    ASSERT_NE(mutable_result, nullptr);
    EXPECT_EQ((int)*mutable_result, 4);

    const kth_to_last::Node* const_head = list.get();
    auto const_result = kth_to_last::get_kth_to_last(const_head, 2);
    ASSERT_NE(const_result, nullptr);
    EXPECT_EQ((int)*const_result, 4);
}

TEST(kth_to_last, boundaries) {
    auto list = create_linked_list({10, 20, 30, 40});

    // k = 1: The tail
    auto tail = kth_to_last::get_kth_to_last(list.get(), 1);
    EXPECT_EQ((int)*tail, 40);

    // k = length: The head
    auto head = kth_to_last::get_kth_to_last(list.get(), 4);
    EXPECT_EQ((int)*head, 10);
}

TEST(kth_to_last, sample) {
    auto list = create_linked_list({1, 2, 3, 4, 5});
    auto node = kth_to_last::get_kth_to_last(list.get(), 2);
    ASSERT_TRUE(node);
    EXPECT_EQ((int)*node, 4);
}
