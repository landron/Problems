/*
./design --gtest_filter=LRUCacheTest.Example1
*/
#include <gtest/gtest.h>

#include "002-LRU.h"

/*
    Example 1: Basic eviction with capacity 2
    ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
    [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
    Output: [null, null, null, 1, null, -1, null, -1, 3, 4]
*/
TEST(LRUCacheTest, Example1) {
    LRUCache cache(2);

    cache.put(1, 1);
    cache.put(2, 2);
    EXPECT_EQ(cache.get(1), 1);

    cache.put(3, 3); // evicts 2
    EXPECT_EQ(cache.get(2), -1);

    cache.put(4, 4); // evicts 1
    EXPECT_EQ(cache.get(1), -1);
    EXPECT_EQ(cache.get(3), 3);
    EXPECT_EQ(cache.get(4), 4);
}

// Test 2: Single capacity cache
TEST(LRUCacheTest, SingleCapacity) {
    LRUCache cache(1);

    cache.put(1, 1);
    EXPECT_EQ(cache.get(1), 1);

    cache.put(2, 2); // evicts 1
    EXPECT_EQ(cache.get(1), -1);
    EXPECT_EQ(cache.get(2), 2);
}

// Test 3: Update existing key
TEST(LRUCacheTest, UpdateExistingKey) {
    LRUCache cache(2);

    cache.put(1, 1);
    cache.put(2, 2);

    // Update key 1 with new value
    cache.put(1, 10);
    EXPECT_EQ(cache.get(1), 10);

    cache.put(3, 3); // evicts 2, not 1 (1 was recently used)
    EXPECT_EQ(cache.get(2), -1);
    EXPECT_EQ(cache.get(1), 10);
    EXPECT_EQ(cache.get(3), 3);
}

// Test 4: Get operation updates recency
TEST(LRUCacheTest, GetUpdatesRecency) {
    LRUCache cache(2);

    cache.put(1, 1);
    cache.put(2, 2);

    cache.get(1); // 1 becomes most recently used

    cache.put(3, 3); // evicts 2, not 1
    EXPECT_EQ(cache.get(2), -1);
    EXPECT_EQ(cache.get(1), 1);
}

// Test 5: Multiple operations on same key
TEST(LRUCacheTest, MultipleOperationsSameKey) {
    LRUCache cache(3);

    cache.put(1, 1);
    cache.put(1, 100);
    cache.put(1, 1000);

    EXPECT_EQ(cache.get(1), 1000);

    cache.put(2, 2);
    cache.put(3, 3);
    cache.put(4, 4); // evicts 1

    EXPECT_EQ(cache.get(1), -1);
    EXPECT_EQ(cache.get(2), 2);
    EXPECT_EQ(cache.get(3), 3);
    EXPECT_EQ(cache.get(4), 4);
}

// Test 6: Getting non-existent key
TEST(LRUCacheTest, GetNonexistent) {
    LRUCache cache(2);

    cache.put(1, 1);
    EXPECT_EQ(cache.get(2), -1);
    EXPECT_EQ(cache.get(100), -1);
}

// Test 7: LRU order verification
TEST(LRUCacheTest, LRUOrder) {
    LRUCache cache(3);

    cache.put(1, 1);
    cache.put(2, 2);
    cache.put(3, 3);

    // Access pattern: 1, 2, 3
    // Next eviction should be 1
    cache.put(4, 4);
    EXPECT_EQ(cache.get(1), -1);
    EXPECT_EQ(cache.get(2), 2);
    EXPECT_EQ(cache.get(3), 3);
    EXPECT_EQ(cache.get(4), 4);
}

// Test 8: Large capacity with few operations
TEST(LRUCacheTest, LargeCapacity) {
    LRUCache cache(100);

    for (int i = 0; i < 10; i++) {
        cache.put(i, i * 10);
    }

    for (int i = 0; i < 10; i++) {
        EXPECT_EQ(cache.get(i), i * 10);
    }

    EXPECT_EQ(cache.get(999), -1);
}

// Test 9: Sequential pattern
TEST(LRUCacheTest, SequentialAccess) {
    LRUCache cache(2);

    cache.put(1, 'a');
    cache.put(2, 'b');
    cache.put(3, 'c'); // evicts 1
    cache.put(4, 'd'); // evicts 2

    EXPECT_EQ(cache.get(1), -1);
    EXPECT_EQ(cache.get(2), -1);
    EXPECT_EQ(cache.get(3), 'c');
    EXPECT_EQ(cache.get(4), 'd');
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
