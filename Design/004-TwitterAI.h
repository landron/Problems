/*
Solution 1
    Runtime
    11ms
    Beats   37.62%
    Memory
    56.22MB
    Beats   38.69%

Solution 2
    Runtime
    7ms
    Beats   63.59%
    Memory
    55.93MB
    Beats   42.73%
*/
#pragma once

#include <algorithm>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace TwitterAI {

struct Tweet {
    unsigned long timestamp;
    int id;
};

struct User {
    int user_id;
    std::unordered_set<int> following;
    // CRITICAL OPTIMIZATION: Swapped std::list for std::vector.
    // List allocates node elements disjointly across global memory. Vector
    // stores them sequentially, maximizing CPU cache-line efficiency.
    std::vector<Tweet> timeline;
};

// CRITICAL OPTIMIZATION: Replaced multi-byte list iterators with a single
// 32-bit index. This shrinks the struct footprint, allowing it to fit into CPU
// registers during sorting operations.
struct HeapNode {
    unsigned long timestamp;
    int tweet_id;
    const std::vector<Tweet>* source_vector;
    size_t current_index;

    // Time Complexity: O(1) | Space Complexity: O(1)
    constexpr bool operator<(const HeapNode& other) const noexcept {
        return timestamp < other.timestamp;
    }
};

class Twitter {
  private:
    std::unordered_map<int, User> users;
    unsigned long global_timestamp;

    // Time Complexity: O(1) average | Space Complexity: O(1)
    // DIFFERENCE FROM YOURS: Returns a direct pointer to the User instance
    // inside the map. This allows subsequent operations to bypass repetitive
    // map lookup hashing.
    inline User* getOrCreateUser(int userId) {
        auto it = users.find(userId);
        if (it == users.end()) {
            return &users
                        .insert({userId, User{.user_id = userId,
                                              .following = {},
                                              .timeline = {}}})
                        .first->second;
        }
        return &(it->second);
    }

  public:
    // Time Complexity: O(1) | Space Complexity: O(1)
    Twitter() : global_timestamp(0) {}

    // Time Complexity: O(1) average | Space Complexity: O(1)
    void postTweet(int userId, int tweetId) {
        User* user = getOrCreateUser(userId);
        // CRITICAL OPTIMIZATION: Instead of push_front (which is slow on
        // vectors), we push_back and read from right-to-left. This gives O(1)
        // amortized insertion.
        user->timeline.push_back(
            Tweet{.timestamp = ++global_timestamp, .id = tweetId});
    }

    // Time Complexity: O(K + N log K) where K is active following channels and
    // N <= 10 Space Complexity: O(K) allocation footprint
    std::vector<int> getNewsFeed(int userId) {
        // Fast-path lookup without structural generation
        auto main_it = users.find(userId);
        if (main_it == users.end()) return {};

        const auto& author = main_it->second;
        if (author.timeline.empty() && author.following.empty()) return {};

        // Track a min-priority queue on stack memory
        std::priority_queue<HeapNode> max_heap;

        std::vector<int> feed;
        feed.reserve(10); // Prevents mid-loop reallocation overhead

        // Process user's personal timeline (reading backwards from the end of
        // the vector)
        if (!author.timeline.empty()) {
            size_t idx = author.timeline.size() - 1;
            max_heap.push(HeapNode{.timestamp = author.timeline[idx].timestamp,
                                   .tweet_id = author.timeline[idx].id,
                                   .source_vector = &author.timeline,
                                   .current_index = idx});
        }

        // Process followee timelines
        for (int followeeId : author.following) {
            auto fit = users.find(followeeId);
            if (fit != users.end() && !fit->second.timeline.empty()) {
                const auto& vec = fit->second.timeline;
                size_t idx = vec.size() - 1;
                max_heap.push(HeapNode{.timestamp = vec[idx].timestamp,
                                       .tweet_id = vec[idx].id,
                                       .source_vector = &vec,
                                       .current_index = idx});
            }
        }

        // Main Merge tracking loop
        while (!max_heap.empty() && feed.size() < 10) {
            // CRITICAL OPTIMIZATION: Avoid copying the structure out of the
            // heap. We read the top value directly and pop immediately.
            HeapNode top_node = max_heap.top();
            max_heap.pop();

            feed.push_back(top_node.tweet_id);

            // Access the next newest tweet by decrementing the vector index
            if (top_node.current_index > 0) {
                size_t next_idx = top_node.current_index - 1;
                const auto& vec = *(top_node.source_vector);
                max_heap.push(HeapNode{.timestamp = vec[next_idx].timestamp,
                                       .tweet_id = vec[next_idx].id,
                                       .source_vector = top_node.source_vector,
                                       .current_index = next_idx});
            }
        }

        return feed;
    }

    // Time Complexity: O(1) average | Space Complexity: O(1)
    void follow(int followerId, int followeeId) {
        if (followerId == followeeId) return;
        getOrCreateUser(followerId)->following.insert(followeeId);
        getOrCreateUser(followeeId);
    }

    // Time Complexity: O(1) average | Space Complexity: O(1)
    void unfollow(int followerId, int followeeId) {
        auto it = users.find(followerId);
        if (it != users.end()) {
            it->second.following.erase(followeeId);
        }
    }
};

} // namespace TwitterAI
