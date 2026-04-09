/*
Queue from Two Stacks
https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/queue-from-two-stacks

To achieve amortized O(1), you must keep the elements in the second stack until they
are actually needed or the stack is empty.

Complexity: O(1) amortized Time (all operations) | O(n) Space
Tags: #queue #stack #amortized
Compliance: ruff & pylint clean.
*/

#include <algorithm>
#include <cassert>
#include <cctype>
#include <cstdlib>
#include <iostream>
#include <span>
#include <stack>
#include <string>
#include <string_view>
#include <vector>

#include <gtest/gtest.h>

class Queue {
public:
    void enqueue(int value) {
        stack_in.push(value);
    }

    auto size() const noexcept {
        // size complexity: O(1) Time | O(1) Space
        return stack_in.size() + stack_out.size();
    }

    auto dequeue() {
        transfer();
        auto value = stack_out.top();
        stack_out.pop();
        return value;
    }

    auto peek() {
        transfer();
        return stack_out.top();
    }

private:
    void transfer() {
        if (!stack_out.empty()) return;
        while (!stack_in.empty()) {
            stack_out.push(stack_in.top());
            stack_in.pop();
        }
    }

private:
    std::stack<int> stack_in;
    std::stack<int> stack_out;
};


// This is painful.
auto trim_and_lower(std::string_view str) -> std::string {
    // Trim leading whitespace
    auto start = str.find_first_not_of(" \t\n\r\f\v");
    if (start == std::string_view::npos) return "";
    
    // Trim trailing whitespace
    auto end = str.find_last_not_of(" \t\n\r\f\v");
    str = str.substr(start, end - start + 1);
    
    // Convert to lowercase
    std::string result(str);
    std::transform(result.begin(), result.end(), result.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    return result;
}


auto process(std::span<const std::string> queries, std::span<const int> values) -> std::vector<int> {
    assert (queries.size() == values.size());
    if (queries.empty()) {
        return {};
    }

    auto queue = Queue{};
    std::vector<int> result;
    for (size_t i = 0; i < queries.size(); ++i) {
        const auto query = trim_and_lower(queries[i]);
        const auto value = values[i];

        if (query == "enqueue") {
            queue.enqueue(value);
        } else if (query == "dequeue") {
            result.push_back(queue.dequeue());
        } else if (query == "peek") {
            result.push_back(queue.peek());
        } else if (query == "size") {
            result.push_back(queue.size());
        } else {
            throw std::invalid_argument("Invalid query: " + queries[i]);
        }
    }

    return result;
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
    std::vector<std::string> queries = {
        "enqueue", "enqueue", "enqueue", "dequeue", "dequeue",
        "enqueue", "peek", "size", "dequeue"
    };
    std::vector<int> values = {1, 2, 3, 0, 0, 4, 0, 0, 0};
    auto result = process(queries, values);
    // First dequeue: 1, Second dequeue: 2
    // Peek (at 3): 3, Size: 2 (3 and 4), Last dequeue: 3
    std::vector<int> expected = {1, 2, 3, 2, 3};
    EXPECT_EQ(result, expected);
}

TEST(QueueFromStacks, CaseInsensitiveOperations) {
    std::vector<std::string> queries = {"ENQUEUE", "ENQUEUE", "Dequeue", "PEEK"};
    std::vector<int> values = {42, 99, 0, 0};
    auto result = process(queries, values);
    ASSERT_EQ(result.size(), 2);
    EXPECT_EQ(result[0], 42);
    EXPECT_EQ(result[1], 99);
}

TEST(QueueFromStacks, AlternatingOperations) {
    std::vector<std::string> queries = {
        "enqueue", "peek", "size", "dequeue", "size"
    };
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
    std::vector<std::string> queries = {
        "enqueue", "enqueue", "enqueue", "dequeue", "dequeue", "dequeue"
    };
    std::vector<int> values = {1, 2, 3, 0, 0, 0};
    auto result = process(queries, values);
    std::vector<int> expected = {1, 2, 3};
    EXPECT_EQ(result, expected);
}
