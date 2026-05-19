/*
./design --gtest_filter=TwitterTest.Example1
./design --gtest_filter=TwitterTest.*
*/
#include <gtest/gtest.h>

#include "004-Twitter.h"
#include "004-TwitterAI.h"

// Example 1: Basic posting, feeding, following, and unfollowing
template <typename Twitter>
void runExample1Test() {
    Twitter twitter;

    twitter.postTweet(1, 5);
    std::vector<int> feed1 = twitter.getNewsFeed(1);
    EXPECT_EQ(feed1, std::vector<int>{5});

    twitter.follow(1, 2);
    twitter.postTweet(2, 6);
    std::vector<int> feed2 = twitter.getNewsFeed(1);
    EXPECT_EQ(feed2, (std::vector<int>{6, 5}));

    twitter.unfollow(1, 2);
    std::vector<int> feed3 = twitter.getNewsFeed(1);
    EXPECT_EQ(feed3, std::vector<int>{5});
}

TEST(TwitterTest, Example1) {
    runExample1Test<TwitterMine>();
    runExample1Test<TwitterAI::Twitter>();
}

template <typename Twitter>
void runNewsFeed() {
    Twitter twitter;

    twitter.postTweet(2, 0);
    twitter.postTweet(2, 3);

    twitter.follow(1, 2);
    twitter.follow(3, 1);

    std::vector<int> expected = {3, 0};
    EXPECT_EQ(twitter.getNewsFeed(1), expected);
    EXPECT_EQ(twitter.getNewsFeed(2), expected) << "follows itself";
    EXPECT_EQ(twitter.getNewsFeed(3), std::vector<int>());
}

TEST(TwitterTest, NewsFeed) {
    runNewsFeed<TwitterMine>();
    runNewsFeed<TwitterAI::Twitter>();
}

// Feed max capacity (10) and strict chronological order
template <typename Twitter>
void runMaxFeedCapacityAndOrdering() {
    Twitter twitter;

    // User 2 posts 12 tweets
    for (int i = 1; i <= 12; ++i) {
        twitter.postTweet(2, i);
    }

    // User 1 follows User 2
    twitter.follow(1, 2);

    // Feed must only return the 10 most recent tweets in reverse chronological
    // order
    std::vector<int> expected = {12, 11, 10, 9, 8, 7, 6, 5, 4, 3};
    EXPECT_EQ(twitter.getNewsFeed(1), expected);
    EXPECT_EQ(twitter.getNewsFeed(2), expected) << "follows itself";
}

TEST(TwitterTest, MaxFeedCapacityAndOrdering) {
    runMaxFeedCapacityAndOrdering<TwitterMine>();
    runMaxFeedCapacityAndOrdering<TwitterAI::Twitter>();
}

// Unfollow behavior when feed drops below max capacity (Backfill requirement)
template <typename Twitter>
void runUnfollowWithFeedBackfill() {
    Twitter twitter;

    // User 1 posts old tweets
    twitter.postTweet(1, 101);
    twitter.postTweet(1, 102);

    // User 2 posts newer tweets
    twitter.follow(1, 2);
    twitter.postTweet(2, 201);
    twitter.postTweet(2, 202);

    // Initial feed: [202, 201, 102, 101]
    std::vector<int> feedBefore = {202, 201, 102, 101};
    EXPECT_EQ(twitter.getNewsFeed(1), feedBefore);

    // User 1 unfollows User 2: User 2's tweets must disappear, leaving only
    // User 1's tweets
    twitter.unfollow(1, 2);
    std::vector<int> feedAfter = {102, 101};
    EXPECT_EQ(twitter.getNewsFeed(1), feedAfter);
}

TEST(TwitterTest, UnfollowWithFeedBackfill) {
    runUnfollowWithFeedBackfill<TwitterMine>();
    runUnfollowWithFeedBackfill<TwitterAI::Twitter>();
}

// Test 4: Handling edge cases like self-following, duplicate following, and
// invalid unfollowing
template <typename Twitter>
void runEdgeCasesFollowUnfollow() {
    Twitter twitter;

    twitter.postTweet(1, 11);
    twitter.postTweet(2, 22);

    // Duplicate follow should not alter feed behavior or duplicate records
    twitter.follow(1, 2);
    twitter.follow(1, 2);
    std::vector<int> expectedFeed = {22, 11};
    EXPECT_EQ(twitter.getNewsFeed(1), expectedFeed);

    EXPECT_EQ(twitter.getNewsFeed(3), std::vector<int>())
        << "getNewsFeed for unexistent works";

    // Unfollowing unexistent
    twitter.unfollow(4, 3);
    twitter.unfollow(1, 3);

    // Unfollowing oneself not supported
    return;

    // Unfollowing oneself should execute safely without breaking invariants
    twitter.unfollow(1, 1);
    std::vector<int> selfFeed = {11};
    EXPECT_EQ(twitter.getNewsFeed(1), selfFeed);
}

TEST(TwitterTest, EdgeCasesFollowUnfollow) {
    runEdgeCasesFollowUnfollow<TwitterMine>();
    runEdgeCasesFollowUnfollow<TwitterAI::Twitter>();
}

// Feed max capacity (10) and follow
template <typename Twitter>
void runMaxFeedCapacityAndFollow() {
    Twitter twitter;

    int i = 0;
    for (; i <= 12; ++i) {
        twitter.postTweet(1, i);
    }
    for (; i <= 21; ++i) {
        twitter.postTweet(2, i);
    }

    // User 3 follows 1 and 2
    twitter.follow(3, 1);
    twitter.follow(3, 2);

    // Feed must only return the 10 most recent tweets in reverse chronological
    // order
    std::vector<int> expected = {21, 20, 19, 18, 17, 16, 15, 14, 13, 12};
    EXPECT_EQ(twitter.getNewsFeed(3), expected);
}

TEST(TwitterTest, MaxFeedCapacityAndFollow) {
    runMaxFeedCapacityAndFollow<TwitterMine>();
    runMaxFeedCapacityAndFollow<TwitterAI::Twitter>();
}

// Feed max capacity (10), follow and unfollow
template <typename Twitter>
void runMaxFeedCapacityAndUnfollow() {
    Twitter twitter;

    int i = 0;
    for (; i <= 12; ++i) {
        twitter.postTweet(1, i);
    }
    for (; i <= 21; ++i) {
        twitter.postTweet(2, i);
    }

    // User 3 follows 1 and 2
    twitter.follow(3, 1);
    twitter.follow(3, 2);

    // Feed must only return the 10 most recent tweets in reverse chronological
    // order
    std::vector<int> expected = {21, 20, 19, 18, 17, 16, 15, 14, 13, 12};
    EXPECT_EQ(twitter.getNewsFeed(3), expected);

    twitter.unfollow(3, 2);

    expected = {12, 11, 10, 9, 8, 7, 6, 5, 4, 3};
    EXPECT_EQ(twitter.getNewsFeed(3), expected);
}

TEST(TwitterTest, MaxFeedCapacityAndUnfollow) {
    runMaxFeedCapacityAndUnfollow<TwitterMine>();
    runMaxFeedCapacityAndUnfollow<TwitterAI::Twitter>();
}

// Test 19/20: Complex sequence with interleaving tweets, 10-feed limits, and
// complete unfollow cleanup
template <typename Twitter>
void runComplexInterleavedSequence() {
    Twitter twitter;

    // Mixed posting sequence from User 1 and User 2
    twitter.postTweet(1, 5);
    twitter.postTweet(2, 3);
    twitter.postTweet(1, 101);
    twitter.postTweet(2, 13);
    twitter.postTweet(2, 10);
    twitter.postTweet(1, 2);
    twitter.postTweet(1, 94);
    twitter.postTweet(2, 505);
    twitter.postTweet(1, 333);
    twitter.postTweet(2, 22);
    twitter.postTweet(1, 11);
    twitter.postTweet(1, 205);
    twitter.postTweet(2, 203);
    twitter.postTweet(1, 201);
    twitter.postTweet(2, 213);
    twitter.postTweet(1, 200);
    twitter.postTweet(2, 202);
    twitter.postTweet(1, 204);
    twitter.postTweet(2, 208);
    twitter.postTweet(2, 233);
    twitter.postTweet(1, 222);
    twitter.postTweet(2, 211);

    // 1. Get News Feed for User 1 before following User 2
    // Expected: Only User 1's 10 most recent tweets in reverse chronological
    // order
    std::vector<int> expectedFeed1 = {222, 204, 200, 201, 205,
                                      11,  333, 94,  2,   101};
    EXPECT_EQ(twitter.getNewsFeed(1), expectedFeed1);

    // User 1 follows User 2
    twitter.follow(1, 2);

    // 2. Get News Feed for User 1 after following User 2
    // Expected: Top 10 most recent tweets interleaved from both User 1 and User
    // 2
    std::vector<int> expectedFeed2 = {211, 222, 233, 208, 204,
                                      202, 200, 213, 201, 203};
    EXPECT_EQ(twitter.getNewsFeed(1), expectedFeed2);

    // User 1 unfollows User 2
    twitter.unfollow(1, 2);
    // 3. Get News Feed for User 1 after unfollowing User 2
    // Expected: User 2's tweets are entirely removed.
    EXPECT_EQ(twitter.getNewsFeed(1), expectedFeed1);
}

TEST(TwitterTest, ComplexInterleavedSequence) {
    runComplexInterleavedSequence<TwitterMine>();
    runComplexInterleavedSequence<TwitterAI::Twitter>();
}
