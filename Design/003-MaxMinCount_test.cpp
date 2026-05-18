/*
./design --gtest_filter=AllOneTest.AlternatingOperations
./design --gtest_filter=AllOneTest.*
*/
#include <gtest/gtest.h>

#include "003-MaxMinCount.h"

// Example 1: Basic operations with single and multiple keys
// ["AllOne", "inc", "inc", "getMaxKey", "getMinKey", "inc", "getMaxKey",
// "getMinKey"]
// [[], ["hello"], ["hello"], [], [], ["leet"], [], []]
// Output: [null, null, null, "hello", "hello", null, "hello", "leet"]
TEST(AllOneTest, Example1) {
    AllOne allOne;

    allOne.inc("hello");
    allOne.inc("hello");
    EXPECT_EQ(allOne.getMaxKey(), "hello");
    EXPECT_EQ(allOne.getMinKey(), "hello");

    allOne.inc("leet");
    EXPECT_EQ(allOne.getMaxKey(), "hello");
    EXPECT_EQ(allOne.getMinKey(), "leet");
}

// Test 2: Single key increment and decrement
TEST(AllOneTest, SingleKeyIncrementDecrement) {
    AllOne allOne;

    allOne.inc("key1");
    EXPECT_EQ(allOne.getMaxKey(), "key1");
    EXPECT_EQ(allOne.getMinKey(), "key1");

    allOne.inc("key1");
    EXPECT_EQ(allOne.getMaxKey(), "key1");
    EXPECT_EQ(allOne.getMinKey(), "key1");

    allOne.dec("key1");
    EXPECT_EQ(allOne.getMaxKey(), "key1");
    EXPECT_EQ(allOne.getMinKey(), "key1");
}

// Test 3: Multiple keys with different counts
TEST(AllOneTest, MultipleKeysWithDifferentCounts) {
    AllOne allOne;

    allOne.inc("a");
    allOne.inc("b");
    allOne.inc("b");
    allOne.inc("c");
    allOne.inc("c");
    allOne.inc("c");

    EXPECT_EQ(allOne.getMaxKey(), "c");
    EXPECT_EQ(allOne.getMinKey(), "a");
}

// Test 4: Increment same key multiple times
TEST(AllOneTest, IncrementSameKeyMultipleTimes) {
    AllOne allOne;

    for (int i = 0; i < 5; i++) {
        allOne.inc("repeated");
    }

    EXPECT_EQ(allOne.getMaxKey(), "repeated");
    EXPECT_EQ(allOne.getMinKey(), "repeated");
}

// Test 5: Decrement brings key to zero (removal)
TEST(AllOneTest, DecrementToZero) {
    AllOne allOne;

    allOne.inc("key1");
    allOne.inc("key2");
    allOne.inc("key2");

    allOne.dec("key1");

    EXPECT_EQ(allOne.getMaxKey(), "key2");
    EXPECT_EQ(allOne.getMinKey(), "key2");
}

// Test 6: Multiple keys with same count
TEST(AllOneTest, MultipleKeysWithSameCount) {
    AllOne allOne;

    allOne.inc("a");
    allOne.inc("b");
    allOne.inc("c");

    // All have count 1, should return lexicographically one of them
    std::string maxKey = allOne.getMaxKey();
    std::string minKey = allOne.getMinKey();

    EXPECT_TRUE(maxKey == "a" || maxKey == "b" || maxKey == "c");
    EXPECT_TRUE(minKey == "a" || minKey == "b" || minKey == "c");
}

// Test 7: Complex sequence of operations
TEST(AllOneTest, ComplexSequence) {
    AllOne allOne;

    allOne.inc("a");
    allOne.inc("b");
    allOne.inc("b");
    EXPECT_EQ(allOne.getMaxKey(), "b");
    EXPECT_EQ(allOne.getMinKey(), "a");

    allOne.inc("a");
    allOne.inc("a");
    allOne.dec("b");
    EXPECT_EQ(allOne.getMaxKey(), "a");
    EXPECT_EQ(allOne.getMinKey(), "b");

    allOne.dec("a");
    EXPECT_EQ(allOne.getMaxKey(), "a");
    EXPECT_EQ(allOne.getMinKey(), "b");

    allOne.dec("b");
    EXPECT_EQ(allOne.getMaxKey(), "a");
    EXPECT_EQ(allOne.getMinKey(), "a");
}

// Test 8: Single key with many increments and decrements
TEST(AllOneTest, SingleKeyManyOperations) {
    AllOne allOne;

    for (int i = 0; i < 10; i++) {
        allOne.inc("key");
    }
    EXPECT_EQ(allOne.getMaxKey(), "key");
    EXPECT_EQ(allOne.getMinKey(), "key");

    for (int i = 0; i < 5; i++) {
        allOne.dec("key");
    }
    EXPECT_EQ(allOne.getMaxKey(), "key");
    EXPECT_EQ(allOne.getMinKey(), "key");
}

// Test 9: Alternating operations on different keys
TEST(AllOneTest, AlternatingOperations) {
    AllOne allOne;

    allOne.inc("x");
    allOne.inc("y");
    allOne.inc("x");
    allOne.inc("y");
    allOne.inc("y");
    EXPECT_EQ(allOne.getMaxKey(), "y");
    EXPECT_EQ(allOne.getMinKey(), "x");

    allOne.dec("y");
    auto val = allOne.getMaxKey();
    EXPECT_TRUE(val == "x" || val == "y");
    val = allOne.getMinKey();
    EXPECT_TRUE(val == "x" || val == "y");

    allOne.dec("y");
    EXPECT_EQ(allOne.getMaxKey(), "x");
    EXPECT_EQ(allOne.getMinKey(), "y");
}

// Test 10: Re-increment after decrement to zero
TEST(AllOneTest, ReIncrementAfterDecrement) {
    AllOne allOne;

    allOne.inc("key");
    allOne.dec("key");
    allOne.inc("key");
    allOne.inc("key");
    allOne.inc("other");

    EXPECT_EQ(allOne.getMaxKey(), "key");
    EXPECT_EQ(allOne.getMinKey(), "other");
}

// Test 11: Three keys with varying counts
TEST(AllOneTest, ThreeKeysVaryingCounts) {
    AllOne allOne;

    allOne.inc("apple");
    allOne.inc("banana");
    allOne.inc("banana");
    allOne.inc("cherry");
    allOne.inc("cherry");
    allOne.inc("cherry");

    EXPECT_EQ(allOne.getMaxKey(), "cherry");
    EXPECT_EQ(allOne.getMinKey(), "apple");

    allOne.dec("cherry");
    allOne.dec("cherry");
    EXPECT_EQ(allOne.getMaxKey(), "banana");
    auto val = allOne.getMinKey();
    EXPECT_TRUE(val == "apple" || val == "cherry");
}

// Test 12: Increment then fully decrement all keys
TEST(AllOneTest, IncrementThenDecrementAll) {
    AllOne allOne;

    allOne.inc("a");
    allOne.inc("b");
    allOne.inc("c");

    allOne.dec("a");
    allOne.dec("b");

    // Only "c" remains with count 1
    EXPECT_EQ(allOne.getMaxKey(), "c");
    EXPECT_EQ(allOne.getMinKey(), "c");

    allOne.dec("c");
    // All keys removed, behavior is undefined
    // This test just ensures no crash
}
