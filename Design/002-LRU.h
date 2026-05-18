/*
https://leetcode.com/problems/lru-cache/description/

Runtime
59ms
Beats   86.90%
Memory
173.28MB
Beats   56.39%

Warning:
 * move_top: move (splice), don't allocate (push_front)

#ds_hash
#ds_dll
#tech_hashmap_iterator
#pattern_cache
#algo_lru
*/
#pragma once

#include <list>
#include <unordered_map>

class LRUCache {
  private:
    using CacheMap =
        std::unordered_map<int, std::pair<int, std::list<int>::iterator>>;

  public:
    explicit LRUCache(size_t _capacity) : capacity(_capacity) {
        assert(capacity && "constraint");
    }

    int get(int key) {
        auto it = values.find(key);
        if (it == values.end()) return -1;
        move_top(it);
        return it->second.first;
    }

    void put(int key, int value) {
        auto it = values.find(key);
        if (it != values.end()) {
            move_top(it);

            it->second.first = value;

            return;
        }

        // make place if necessary
        assert(values.size() <= capacity);
        if (capacity == values.size()) {
            values.erase(order.back());
            order.pop_back();
        }

        order.push_front(key);
        values[key] = {value, order.begin()};

        assert(order.size() <= capacity);
        assert(order.size() == values.size());
    }

  private:
    void move_top(CacheMap::iterator it) {
        // no push_front => avoid allocation
        order.splice(order.begin(), order, it->second.second);
        it->second.second = order.begin();
        assert(order.size() == values.size());
    }

  private:
    std::list<int> order; // Tracks the usage order (Front = Most Recent, Back =
                          // Least Recent)
    CacheMap values;      // Provides O(1) lookups
    const size_t capacity;
};
