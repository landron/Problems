#include "001-RandomizedSet.h"
#include <gtest/gtest.h>
#include <set>

class RandomizedSetTest : public ::testing::Test {
  protected:
    RandomizedSet rs;
};

// Test insert functionality
TEST_F(RandomizedSetTest, InsertSingleElement) {
    EXPECT_TRUE(rs.insert(1));
}

TEST_F(RandomizedSetTest, InsertDuplicateReturnsFalse) {
    EXPECT_TRUE(rs.insert(5));
    EXPECT_FALSE(rs.insert(5));
}

TEST_F(RandomizedSetTest, InsertMultipleElements) {
    EXPECT_TRUE(rs.insert(1));
    EXPECT_TRUE(rs.insert(2));
    EXPECT_TRUE(rs.insert(3));
    EXPECT_FALSE(rs.insert(1));
    EXPECT_FALSE(rs.insert(2));
}

// Test remove functionality
TEST_F(RandomizedSetTest, RemoveNonExistentReturnsFalse) {
    EXPECT_FALSE(rs.remove(1));
}

TEST_F(RandomizedSetTest, RemoveSingleElement) {
    EXPECT_TRUE(rs.insert(7));
    EXPECT_TRUE(rs.remove(7));
    EXPECT_FALSE(rs.remove(7));
}

TEST_F(RandomizedSetTest, RemoveMultipleElements) {
    EXPECT_TRUE(rs.insert(1));
    EXPECT_TRUE(rs.insert(2));
    EXPECT_TRUE(rs.insert(3));

    EXPECT_TRUE(rs.remove(2));
    EXPECT_FALSE(rs.remove(2));

    EXPECT_TRUE(rs.remove(1));
    EXPECT_FALSE(rs.remove(1));

    EXPECT_TRUE(rs.remove(3));
    EXPECT_FALSE(rs.remove(3));
}

TEST_F(RandomizedSetTest, RemoveFirstElement) {
    EXPECT_TRUE(rs.insert(10));
    EXPECT_TRUE(rs.insert(20));
    EXPECT_TRUE(rs.remove(10));
}

TEST_F(RandomizedSetTest, RemoveLastElement) {
    EXPECT_TRUE(rs.insert(10));
    EXPECT_TRUE(rs.insert(20));
    EXPECT_TRUE(rs.remove(20));
}

TEST_F(RandomizedSetTest, RemoveMiddleElement) {
    EXPECT_TRUE(rs.insert(10));
    EXPECT_TRUE(rs.insert(20));
    EXPECT_TRUE(rs.insert(30));
    EXPECT_TRUE(rs.remove(20));
}

// Test getRandom functionality
TEST_F(RandomizedSetTest, GetRandomAfterInsert) {
    EXPECT_TRUE(rs.insert(42));
    EXPECT_EQ(rs.getRandom(), 42);
}

TEST_F(RandomizedSetTest, GetRandomReturnsValidElement) {
    std::set<int> inserted = {1, 5, 10, 15, 20};
    for (int val : inserted) {
        EXPECT_TRUE(rs.insert(val));
    }

    // Call getRandom multiple times to ensure all elements can be returned
    std::set<int> returned;
    for (int i = 0; i < 1000; ++i) {
        int val = rs.getRandom();
        EXPECT_TRUE(inserted.count(val) > 0);
        returned.insert(val);
    }

    // With high probability, we should see multiple different elements
    // (not guaranteed, but extremely likely with 1000 calls)
    EXPECT_GT(returned.size(), 1);
}

// Test combined operations
TEST_F(RandomizedSetTest, CombinedInsertRemoveGetRandom) {
    EXPECT_TRUE(rs.insert(1));
    EXPECT_TRUE(rs.insert(2));
    auto val = rs.getRandom();
    EXPECT_TRUE(val == 1 || val == 2)
        << "getRandom should return one of {1, 2}";

    EXPECT_TRUE(rs.remove(1));
    EXPECT_EQ(rs.getRandom(), 2)
        << "After removing 1, getRandom should return 2";
}

TEST_F(RandomizedSetTest, ComplexSequence) {
    EXPECT_TRUE(rs.insert(5));
    EXPECT_TRUE(rs.insert(10));
    EXPECT_TRUE(rs.insert(15));

    EXPECT_TRUE(rs.remove(10));
    EXPECT_TRUE(rs.insert(20));

    // Should contain {5, 15, 20}
    std::set<int> values;
    for (int i = 0; i < 100; ++i) {
        values.insert(rs.getRandom());
    }
    EXPECT_EQ(values.size(), 3);
    EXPECT_TRUE(values.count(5) > 0);
    EXPECT_TRUE(values.count(15) > 0);
    EXPECT_TRUE(values.count(20) > 0);
}

// Test edge cases
TEST_F(RandomizedSetTest, InsertNegativeNumbers) {
    EXPECT_TRUE(rs.insert(-1));
    EXPECT_TRUE(rs.insert(-100));
    auto val = rs.getRandom();
    EXPECT_TRUE(val == -1 || val == -100)
        << "getRandom should return one of {-1, -100}";
}

TEST_F(RandomizedSetTest, InsertZero) {
    EXPECT_TRUE(rs.insert(0));
    EXPECT_EQ(rs.getRandom(), 0);
}

TEST_F(RandomizedSetTest, InsertLargeNumbers) {
    EXPECT_TRUE(rs.insert(1000000));
    EXPECT_TRUE(rs.insert(-1000000));
    std::set<int> values;
    for (int i = 0; i < 10; ++i) {
        values.insert(rs.getRandom());
    }
    EXPECT_EQ(values.size(), 2);
}
