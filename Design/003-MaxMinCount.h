/*
https://leetcode.com/problems/all-oone-data-structure/

Why your multimap solution scores better sometimes

Your first version (AllOne1):
* fewer allocations
* simpler structure
* better cache locality
* STL-balanced tree is highly optimized in C++
So it can beat “O(1)” solutions in practice.

#ds_hash
#ds_dll
#ds_bucket
#tech_hashmap_iterator
#tech_bucket_list
#pattern_frequency
*/
#pragma once

#include <list>
#include <string>
#include <unordered_set>

/*
Runtime
73ms
Beats   71.95%
Memory
94.72MB
Beats   29.93%

TODO: Improve:
    list<string> inside Bucket
    map<string, <Bucket, iterator inside list<string> >>
*/
class AllOne_Amortized {
  private:
    struct Bucket {
        size_t count;
        std::unordered_set<std::string> data;
    };
    using Order = std::list<Bucket>;

  public:
    // O(1) amortized time
    void inc(const std::string& key) {
        Order::iterator where;
        auto found = data.find(key);
        if (found == data.end()) {
            where = bucket_first();
            data[key] = where;
        } else {
            where = bucket_adjacent(found->second, true, key);
            found->second = where;
        }
        where->data.insert(key);
    }

    // O(1) amortized time
    void dec(const std::string& key) {
        auto found = data.find(key);
        assert(found != data.end() && "constraint");

        if (1 == found->second->count) {
            bucket_remove(key, found->second);
            data.erase(found);
            return;
        }
        auto where = bucket_adjacent(found->second, false, key);
        found->second = where;
        where->data.insert(key);
    }

    // O(1)
    std::string getMaxKey() {
        if (data.empty()) return "";
        return *(std::prev(order.end())->data.begin());
    }

    // O(1)
    std::string getMinKey() {
        if (data.empty()) return "";
        return *(order.begin()->data.begin());
    }

  private:
    Order::iterator bucket_first(size_t count = 1) {
        if (order.empty() || order.begin()->count > 1)
            order.push_front({count, {}});
        return order.begin();
    }
    Order::iterator bucket_adjacent(Order::iterator it, bool inc,
                                    const std::string& key) {
        auto where = bucket_add(it, inc);
        bucket_remove(key, it);
        return where;
    }
    Order::iterator bucket_add(Order::iterator it, bool inc) {
        assert(it != order.end());
        const auto count = inc ? it->count + 1 : it->count - 1;

        if (inc) {
            auto next = std::next(it);
            if (next == order.end() || next->count > count)
                order.insert(next, {count, {}});
            return std::next(it);
        }

        assert(it->count > count);
        if (it == order.begin()) {
            order.push_front({count, {}});
            return order.begin();
        }
        auto prev = std::prev(it);
        if (prev->count < count) order.insert(it, {count, {}});
        return std::prev(it);
    }
    void bucket_remove(const std::string& key, Order::iterator it) {
        it->data.erase(key);
        if (it->data.empty()) order.erase(it);
    }

  private:
    std::unordered_map<std::string, Order::iterator> data;
    Order order;
};

/*
Runtime
66ms
Beats   85.53%
Memory
84.98MB
Beats   90.49%
*/
class AllOne_NotO1 {
  public:
    // O(log n)
    void inc(const std::string& key) {
        auto found = data.find(key);
        size_t cnt = 1;
        if (found != data.end()) {
            order.erase(found->second.second);
            cnt = ++found->second.first;
        }
        auto it = order.insert({cnt, key});
        data[key] = {cnt, it};
    }

    // O(log n)
    void dec(const std::string& key) {
        auto found = data.find(key);
        assert(found != data.end() && "constraint");
        order.erase(found->second.second);
        auto cnt = --found->second.first;
        if (cnt == 0) {
            data.erase(found);
            return;
        }
        auto it = order.insert({cnt, key});
        data[key] = {cnt, it};
    }

    // O(1)
    std::string getMaxKey() {
        if (data.empty()) return "";
        return std::prev(order.end())->second;
    }

    // O(1)
    std::string getMinKey() {
        if (data.empty()) return "";
        return order.begin()->second;
    }

  private:
    using Order = std::multimap<size_t, std::string>;
    std::unordered_map<std::string, std::pair<size_t, Order::iterator>> data;
    Order order;
};
