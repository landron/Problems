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
template <typename AllOne>
void runExample1() {
    AllOne allOne;

    allOne.inc("hello");
    allOne.inc("hello");
    EXPECT_EQ(allOne.getMaxKey(), "hello");
    EXPECT_EQ(allOne.getMinKey(), "hello");

    allOne.inc("leet");
    EXPECT_EQ(allOne.getMaxKey(), "hello");
    EXPECT_EQ(allOne.getMinKey(), "leet");
}

TEST(AllOneTest, Example1) {
    runExample1<AllOne_NotO1>();
    runExample1<AllOne_Amortized>();
}

// Test 2: Single key increment and decrement
template <typename AllOne>
void runSingleKeyIncrementDecrement() {
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

TEST(AllOneTest, SingleKeyIncrementDecrement) {
    runSingleKeyIncrementDecrement<AllOne_NotO1>();
    runSingleKeyIncrementDecrement<AllOne_Amortized>();
}

// Test 3: Multiple keys with different counts
template <typename AllOne>
void runMultipleKeysWithDifferentCounts() {
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

TEST(AllOneTest, MultipleKeysWithDifferentCounts) {
    runMultipleKeysWithDifferentCounts<AllOne_NotO1>();
    runMultipleKeysWithDifferentCounts<AllOne_Amortized>();
}

// Test 4: Increment same key multiple times
template <typename AllOne>
void runIncrementSameKeyMultipleTimes() {
    AllOne allOne;

    for (int i = 0; i < 5; i++) {
        allOne.inc("repeated");
    }

    EXPECT_EQ(allOne.getMaxKey(), "repeated");
    EXPECT_EQ(allOne.getMinKey(), "repeated");
}

TEST(AllOneTest, IncrementSameKeyMultipleTimes) {
    runIncrementSameKeyMultipleTimes<AllOne_NotO1>();
    runIncrementSameKeyMultipleTimes<AllOne_Amortized>();
}

// Test 5: Decrement brings key to zero (removal)
template <typename AllOne>
void runDecrementToZero() {
    AllOne allOne;

    allOne.inc("key1");
    allOne.inc("key2");
    allOne.inc("key2");

    allOne.dec("key1");

    EXPECT_EQ(allOne.getMaxKey(), "key2");
    EXPECT_EQ(allOne.getMinKey(), "key2");
}

TEST(AllOneTest, DecrementToZero) {
    runDecrementToZero<AllOne_NotO1>();
    runDecrementToZero<AllOne_Amortized>();
}

// Test 6: Multiple keys with same count
template <typename AllOne>
void runMultipleKeysWithSameCount() {
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

TEST(AllOneTest, MultipleKeysWithSameCount) {
    runMultipleKeysWithSameCount<AllOne_NotO1>();
    runMultipleKeysWithSameCount<AllOne_Amortized>();
}

// Test 7: Complex sequence of operations
template <typename AllOne>
void runComplexSequence() {
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

TEST(AllOneTest, ComplexSequence) {
    runComplexSequence<AllOne_NotO1>();
    runComplexSequence<AllOne_Amortized>();
}

// Test 8: Single key with many increments and decrements
template <typename AllOne>
void runSingleKeyManyOperations() {
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

TEST(AllOneTest, SingleKeyManyOperations) {
    runSingleKeyManyOperations<AllOne_NotO1>();
    runSingleKeyManyOperations<AllOne_Amortized>();
}

// Test 9: Alternating operations on different keys
template <typename AllOne>
void runAlternatingOperations() {
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

TEST(AllOneTest, AlternatingOperations) {
    runAlternatingOperations<AllOne_NotO1>();
    runAlternatingOperations<AllOne_Amortized>();
}

// Test 10: Re-increment after decrement to zero
template <typename AllOne>
void runReIncrementAfterDecrement() {
    AllOne allOne;

    allOne.inc("key");
    allOne.dec("key");
    allOne.inc("key");
    allOne.inc("key");
    allOne.inc("other");

    EXPECT_EQ(allOne.getMaxKey(), "key");
    EXPECT_EQ(allOne.getMinKey(), "other");
}

TEST(AllOneTest, ReIncrementAfterDecrement) {
    runReIncrementAfterDecrement<AllOne_NotO1>();
    runReIncrementAfterDecrement<AllOne_Amortized>();
}

// Test 11: Three keys with varying counts
template <typename AllOne>
void runThreeKeysVaryingCounts() {
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

TEST(AllOneTest, ThreeKeysVaryingCounts) {
    runThreeKeysVaryingCounts<AllOne_NotO1>();
    runThreeKeysVaryingCounts<AllOne_Amortized>();
}

// Test 12: Increment then fully decrement all keys
template <typename AllOne>
void runIncrementThenDecrementAll() {
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

TEST(AllOneTest, IncrementThenDecrementAll) {
    runIncrementThenDecrementAll<AllOne_NotO1>();
    runIncrementThenDecrementAll<AllOne_Amortized>();
}
