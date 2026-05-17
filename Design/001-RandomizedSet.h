/*
https://leetcode.com/problems/insert-delete-getrandom-o1/description/

Runtime
38ms
Beats   79.36%
Memory
113.63MB
Beats   8.68%

#ds_hash
#ds_vector
#tech_hashmap_index
*/

#include <cassert>
#include <random>
#include <unordered_map>
#include <vector>

class RandomizedSet {
  public:
    RandomizedSet() : gen(std::random_device{}()) {}

    bool insert(int val) {
        auto [it, inserted] = position.emplace(val, numbers.size());
        if (!inserted) return false;

        numbers.push_back(val);
        return true;
    }

    bool remove(int val) {
        auto it = position.find(val);
        if (it == position.end()) return false;

        // just swap with the last to keep positions
        position[numbers.back()] = it->second;
        numbers[it->second] = numbers.back();

        // remove old element
        position.erase(it);
        numbers.pop_back();

        return true;
    }

    int getRandom() {
        assert(!numbers.empty() && "constraint");
        std::uniform_int_distribution<> dist(0, numbers.size() - 1);
        return numbers[dist(gen)];
    }

  private:
    std::unordered_map<int, int> position;
    std::vector<int> numbers;
    std::mt19937 gen;
};
