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
    4ms
    Beats   82.27%
    Memory
    56.00MB
    Beats   40.94%

#ds_hash
#ds_heap
#ds_vector
#ds_graph       # followers: directed graph adjacency list
#algo_kway_merge
#tech_cache_locality
#tech_heap_merge
#tech_reverse_traversal
#tech_index_pointer
#design_social_feed
#design_twitter
#perf_allocator
#perf_cache_friendly
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
    std::unordered_set<int> following;
    // Cache Locality
    // CRITICAL OPTIMIZATION: Swapped std::list for std::vector.
    // List allocates node elements disjointly across global memory. Vector
    // stores them sequentially, maximizing CPU cache-line efficiency.
    //
    // ChatGPT: This is probably the single biggest real-world win.
    std::vector<Tweet> timeline;
};

// CRITICAL OPTIMIZATION: Replaced multi-byte list iterators with a single
// 32-bit index. This shrinks the struct footprint, allowing it to fit into CPU
// registers during sorting operations.
struct HeapNode {
    unsigned long timestamp;
    int tweet_id;
    const std::vector<Tweet>* source_vector;
    // ChatGPT: Excellent micro-optimization.
    size_t current_index;

    // Time Complexity: O(1) | Space Complexity: O(1)
    constexpr bool operator<(const HeapNode& other) const noexcept {
        return timestamp < other.timestamp;
    }
};

class Twitter {
  private:
    std::unordered_map<int, User> users;
    unsigned long global_timestamp = 0;

    // Time Complexity: O(1) average | Space Complexity: O(1)
    // DIFFERENCE FROM YOURS: Returns a direct pointer to the User instance
    // inside the map. This allows subsequent operations to bypass repetitive
    // map lookup hashing.
    inline User* getOrCreateUser(int userId) {
        auto it = users.find(userId);
        if (it == users.end())
            return &users.insert({userId, User{}}).first->second;
        return &(it->second);
    }

  public:
    // Time Complexity: O(1) average | Space Complexity: O(1)
    void postTweet(int userId, int tweetId) {
        auto user = getOrCreateUser(userId);
        // CRITICAL OPTIMIZATION: Instead of push_front (which is slow on
        // vectors), we push_back and read from right-to-left. This gives O(1)
        // amortized insertion.
        user->timeline.push_back(
            Tweet{.timestamp = ++global_timestamp, .id = tweetId});
    }

    // Time Complexity: O(K * log K) where K is active following channels
    // and N <= 10
    //  *  Initial heap population: O((K+1) * log K)
    //  *  Main loop: O(N log K)
    // Space Complexity: O(K) allocation footprint
    /*
        priority_queue vs map
        Both approaches achieve $O(\log K)$ time complexity per operation, but
       they have fundamentally different hardware and execution
       characteristics:
       * std::priority_queue (Binary Heap):Same $O(\log K)$, but
       blazing fast. It operates inside a contiguous block of memory with zero
       dynamic allocations during the tracking loop, making it highly friendly
       to your CPU cache.std::map (Red-Black Tree):Same $O(\log K)$, but
       sluggish. Every single insertion or deletion forces the OS to allocate or
       free dynamic memory node structures, while pointer chasing degrades CPU
       cache efficiency.
     */
    std::vector<int> getNewsFeed(int userId) {
        auto get_user = [&]() -> const User* {
            auto it = users.find(userId);
            if (it == users.end()) return nullptr;
            return &(it->second);
        };
        auto reader = get_user();
        if (!reader) return {};

        if (reader->timeline.empty() && reader->following.empty()) return {};

        // Track a min-priority queue on stack memory
        std::priority_queue<HeapNode> max_heap;

        std::vector<int> feed;
        feed.reserve(10); // Prevents mid-loop reallocation overhead

        auto add_to_heap = [&](const std::vector<Tweet>& timeline, size_t idx) {
            max_heap.push(HeapNode{.timestamp = timeline[idx].timestamp,
                                   .tweet_id = timeline[idx].id,
                                   .source_vector = &timeline,
                                   .current_index = idx});
        };
        auto add_last_to_heap = [&](const std::vector<Tweet>& timeline) {
            return add_to_heap(timeline, timeline.size() - 1);
        };

        // Process user's personal timeline (reading backwards from the end of
        // the vector)
        //  adds newest (latest) node only
        if (!reader->timeline.empty()) add_last_to_heap(reader->timeline);

        // Process followee timelines
        for (auto followeeId : reader->following) {
            auto it = users.find(followeeId);
            if (it != users.end() && !it->second.timeline.empty())
                add_last_to_heap(it->second.timeline);
        }

        // Main Merge tracking loop
        while (!max_heap.empty() && feed.size() < 10) {
            // CRITICAL OPTIMIZATION: Avoid copying the structure out of the
            // heap. We read the top value directly and pop immediately.
            HeapNode top_node = max_heap.top();
            max_heap.pop();

            feed.push_back(top_node.tweet_id);

            // Access the next newest tweet by decrementing the vector index
            if (top_node.current_index > 0)
                add_to_heap(*(top_node.source_vector),
                            top_node.current_index - 1);
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
