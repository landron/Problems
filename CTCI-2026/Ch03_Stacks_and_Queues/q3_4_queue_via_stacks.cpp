/*
Queue from Two Stacks
https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/queue-from-two-stacks

To achieve amortized O(1), you must keep the elements in the second stack until
they are actually needed or the stack is empty.

Complexity: O(1) amortized Time (all operations) | O(n) Space
Tags: #queue #stack #amortized
Style: clang-format clean. (ninja format)

Modern C++ best practices:
- Use std::expected for operations that may fail (e.g., dequeue on empty queue).
- Use std::span for input parameters to allow flexible array-like inputs.
- Use std::move and perfect forwarding for efficient value handling.
- Use pipelining, views and ranges for string processing to improve readability
and maintainability.
    * see trim_and_lower
    * instantiate with std::string_view for zero-copy processing.
#modern_cpp #cpp23
*/

#include <cassert>
#include <concepts>
#include <expected>
#include <span>
#include <stack>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

#include <gtest/gtest.h>

#include "strings_op.hpp"

template <std::move_constructible T>
class Queue {
  public:
    enum class QueueError {
        Empty, // empty queue on peek/dequeue
    };

    void enqueue(T value) {
        stack_in.push(std::move(value));
    }

    template <typename... Args>
    void emplace(Args&&... args) {
        stack_in.emplace(std::forward<Args>(args)...);
    }

    [[nodiscard]] std::size_t size() const noexcept {
        // size complexity: O(1) Time | O(1) Space
        return stack_in.size() + stack_out.size();
    }

    // no [[nodiscard]]: caller may ignore result for fire-and-forget dequeues
    std::expected<T, QueueError>
    dequeue() noexcept(std::is_nothrow_move_constructible_v<T>) {
        transfer();
        if (stack_out.empty()) return std::unexpected(QueueError::Empty);
        auto value = std::move(stack_out.top());
        stack_out.pop();
        return value;
    }

    // const method: mutable stacks allow lazy transfer without const_cast
    // (logical const)
    [[nodiscard]] std::expected<T, QueueError> peek() const
        noexcept(std::is_nothrow_move_constructible_v<T>) {
        transfer();
        if (stack_out.empty()) return std::unexpected(QueueError::Empty);
        return stack_out.top();
    }

  private:
    void transfer() const noexcept(std::is_nothrow_move_constructible_v<T>) {
        if (!stack_out.empty()) return;
        while (!stack_in.empty()) {
            stack_out.push(std::move(stack_in.top()));
            stack_in.pop();
        }
    }

  private:
    mutable std::stack<T> stack_in;
    mutable std::stack<T> stack_out;
};

auto process(std::span<const std::string> queries, std::span<const int> values)
    -> std::vector<int> {
    assert(queries.size() == values.size());

    auto queue = Queue<int>{};
    std::vector<int> result;
    result.reserve(queries.size());

    // const auto& can fail on temporary objects returned by modern views;
    // auto&& never does.
    for (auto&& [query_str, value] : std::views::zip(queries, values)) {
        auto query = trim_and_lower(query_str);

        if (view_eq(query, "enqueue")) {
            queue.enqueue(value);
        } else if (view_eq(query, "dequeue")) {
            // safe to dereference: crashes allowed for invalid ops
            result.push_back(*queue.dequeue());
        } else if (view_eq(query, "peek")) {
            // safe to dereference: crashes allowed for invalid ops
            result.push_back(*queue.peek());
        } else if (view_eq(query, "size")) {
            result.push_back(static_cast<int>(queue.size()));
        } else {
            throw std::invalid_argument("Invalid query: " + query_str);
        }
    }

    return result;
}

TEST(Queue, DequeueEmptyReturnsError) {
    Queue<int> q;
    auto result = q.dequeue();
    ASSERT_FALSE(result.has_value());
    EXPECT_EQ(result.error(), Queue<int>::QueueError::Empty);
}

TEST(Queue, PeekEmptyReturnsError) {
    Queue<int> q;
    auto result = q.peek();
    ASSERT_FALSE(result.has_value());
    EXPECT_EQ(result.error(), Queue<int>::QueueError::Empty);
}

TEST(Queue, DequeueReturnsValue) {
    Queue<int> q;
    q.enqueue(42);
    auto result = q.dequeue();
    ASSERT_TRUE(result.has_value());
    EXPECT_EQ(*result, 42);
}

TEST(Queue, PeekReturnsValueWithoutRemoving) {
    Queue<int> q;
    q.enqueue(42);
    ASSERT_TRUE(q.peek().has_value());
    EXPECT_EQ(*q.peek(), 42);
    EXPECT_EQ(q.size(), 1); // still in queue
}

TEST(Queue, DequeueUntilEmptyThenError) {
    Queue<int> q;
    q.enqueue(1);
    q.enqueue(2);
    EXPECT_TRUE(q.dequeue().has_value());
    EXPECT_TRUE(q.dequeue().has_value());
    auto result = q.dequeue();
    ASSERT_FALSE(result.has_value());
    EXPECT_EQ(result.error(), Queue<int>::QueueError::Empty);
}

TEST(QueueFromStacks, EmptyOperations) {
    std::vector<std::string> queries;
    std::vector<int> values;
    auto result = process(queries, values);
    EXPECT_EQ(result, std::vector<int>{});
}

TEST(QueueFromStacks, SingleEnqueue) {
    std::vector<std::string> queries = {"enqueue"};
    std::vector<int> values = {5};
    auto result = process(queries, values);
    EXPECT_EQ(result, std::vector<int>{});
}

TEST(QueueFromStacks, EnqueueDequeue) {
    std::vector<std::string> queries = {"enqueue", "dequeue"};
    std::vector<int> values = {10, 0};
    auto result = process(queries, values);
    EXPECT_EQ(result, std::vector<int>{10});
}

TEST(QueueFromStacks, SizeOperation) {
    std::vector<std::string> queries = {"enqueue", "enqueue", "size"};
    std::vector<int> values = {1, 2, 0};
    auto result = process(queries, values);
    EXPECT_EQ(result, std::vector<int>{2});
}

TEST(QueueFromStacks, PeekOperation) {
    std::vector<std::string> queries = {"enqueue", "enqueue", "peek"};
    std::vector<int> values = {7, 8, 0};
    auto result = process(queries, values);
    EXPECT_EQ(result, std::vector<int>{7});
}

TEST(QueueFromStacks, ComplexSequence) {
    std::vector<std::string> queries = {"enqueue", "enqueue", "enqueue",
                                        "dequeue", "dequeue", "enqueue",
                                        "peek",    "size",    "dequeue"};
    std::vector<int> values = {1, 2, 3, 0, 0, 4, 0, 0, 0};
    auto result = process(queries, values);
    // First dequeue: 1, Second dequeue: 2
    // Peek (at 3): 3, Size: 2 (3 and 4), Last dequeue: 3
    std::vector<int> expected = {1, 2, 3, 2, 3};
    EXPECT_EQ(result, expected);
}

TEST(QueueFromStacks, CaseInsensitiveOperations) {
    std::vector<std::string> queries = {"ENQUEUE", "ENQUEUE", "Dequeue",
                                        "PEEK"};
    std::vector<int> values = {42, 99, 0, 0};
    auto result = process(queries, values);
    ASSERT_EQ(result.size(), 2);
    EXPECT_EQ(result[0], 42);
    EXPECT_EQ(result[1], 99);
}

TEST(QueueFromStacks, AlternatingOperations) {
    std::vector<std::string> queries = {"enqueue", "peek", "size", "dequeue",
                                        "size"};
    std::vector<int> values = {10, 0, 0, 0, 0};
    auto result = process(queries, values);
    std::vector<int> expected = {10, 1, 10, 0};
    EXPECT_EQ(result, expected);
}

TEST(QueueFromStacks, MultiplePeeksSameElement) {
    std::vector<std::string> queries = {"enqueue", "peek", "peek", "peek"};
    std::vector<int> values = {42, 0, 0, 0};
    auto result = process(queries, values);
    std::vector<int> expected = {42, 42, 42};
    EXPECT_EQ(result, expected);
}

TEST(QueueFromStacks, FIFOOrder) {
    std::vector<std::string> queries = {"enqueue", "enqueue", "enqueue",
                                        "dequeue", "dequeue", "dequeue"};
    std::vector<int> values = {1, 2, 3, 0, 0, 0};
    auto result = process(queries, values);
    std::vector<int> expected = {1, 2, 3};
    EXPECT_EQ(result, expected);
}
