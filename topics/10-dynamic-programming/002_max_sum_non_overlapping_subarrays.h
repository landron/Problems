/*
https://leetcode.com/problems/maximum-sum-of-m-non-overlapping-subarrays-i
*/
/*
    Vector of size n, search 1 to m subarrays where l <= size <= r
    Goal: Maximize total sum. Return maximum sum value.

    Dynamic programming solution - 2D array calculation
    DP[i][j]: max sum starting at index i with j subarrays remaining
        (n+2) x (m+1) space
        * j : 1 -> m
        * i : n-l -> 0 (backwards)

    Base Case: DP[i][0] = 0 for all i (0 subarrays selected yields 0 sum)
    Result: max (1 <= j <= m) (DP[0][j])

    SolutionDP:
        O(m * n * (r - l + 1)) : last term can be optimized later

        DP[i][j] calculation:
            max of:
                DP[i+1][j] : skip current element (not necessarily negative)
                max_{l <= k <= r} (Sum(i, i+k-1) + DP[i+k][j-1]) :
                    take subarray of length k

                Sum(i, i+k-1) depends on i => must be calculated each time i
                changes.

    SolutionPrecalculatedSubarrays (Monotonic Queue Optimization):
        O(m * n) time, O(m * n) space

        Formula Transformation:
            Let P be the prefix sum array of nums.
            Sum(i, i+k-1) = P[i+k] - P[i]
            Target = max_{l <= k <= r} (P[i+k] + DP[i+k][j-1]) - P[i]

            (P[x] + DP[x][j-1]) is simply a sliding window, so it avoids (r-l+1)
            calculations from the previous.

        DP[i][j] calculation:
            max of:
                DP[i+1][j] : skip current element
                (dq.front() value) - P[i] :
                    where dq maintains the maximum of (P[x] + DP[x][j-1])
                    for x in range [i+l, i+r]
*/
/*
#algo_dynamic_programming
#dp_interval_choice
#algo_prefix_sum_trick
#algo_sliding_window_maximum
#algo_monotonic_queue
#tech_state_transition_rewrite
#opt_range_max_query
#pattern_dp_knapsack_variant
#perf_o_mn_optimization
*/
#pragma once

#include <algorithm>
#include <deque>
#include <numeric>
#include <vector>

// Gemini optimization
class SolutionPrecalculatedSubarrays {
  public:
    static long long maximumSum(const std::vector<int>& nums, size_t m,
                                size_t l, size_t r) {
        const size_t n = nums.size();

        std::vector<long long> pref(n + 1, 0);
        for (size_t i = 0; i < n; ++i)
            pref[i + 1] = pref[i] + nums[i];

        std::vector<std::vector<long long>> dp(
            n + 2, std::vector<long long>(m + 1, 0));
        // Use an explicit reachability table to prevent underflow
        std::vector<std::vector<bool>> reachable(
            n + 2, std::vector<bool>(m + 1, false));

        for (size_t i = 0; i <= n + 1; ++i)
            reachable[i][0] = true;

        for (size_t j = 1; j <= m; ++j) {
            // Monotonic queue storing array indices to track the maximum value
            // of (pref[x] + dp[x][j-1]) within the sliding window [i + l, i +
            // r]. Sorted in descending order of value to look up the optimal
            // transition in O(1).
            std::deque<size_t> dq;

            // Use an int loop to safely match size_t values without underflow
            // drops
            for (int i = (int)n; i >= 0; --i) {
                const auto add_idx = i + l;
                const auto rem_idx = i + r;

                // Add to window only if state is genuinely reachable
                if (add_idx <= n && reachable[add_idx][j - 1]) {
                    const auto val = pref[add_idx] + dp[add_idx][j - 1];
                    while (!dq.empty()) {
                        const auto back = dq.back();
                        const auto back_val = pref[back] + dp[back][j - 1];
                        if (back_val > val) break;
                        dq.pop_back();
                    }
                    dq.push_back(add_idx);
                }

                // Remove out-of-range elements
                if (!dq.empty() && dq.front() > rem_idx) dq.pop_front();

                // set DP[i][j]

                // max(dp[i + 1][j] - skip element, max subarray)
                // Option 1: Skip
                auto best = dp[i + 1][j];
                auto valid = reachable[i + 1][j];
                // Option 2: Subarray window
                if (!dq.empty()) {
                    const auto x = dq.front();
                    const auto current_option =
                        pref[x] + dp[x][j - 1] - pref[i];
                    if (!valid || current_option > best) {
                        best = current_option;
                        valid = true;
                    }
                }
                if (valid) {
                    dp[i][j] = best;
                    reachable[i][j] = true;
                }
            }
        }

        auto get_max_by_subarrays_count = [&]() {
            auto valid = false;
            auto best = static_cast<long long>(0);
            for (size_t j = 1; j <= m; ++j) {
                if (!reachable[0][j]) continue;
                if (!valid || best < dp[0][j]) best = dp[0][j];
                valid = true;
            }
            return best;
        };
        return get_max_by_subarrays_count();
    }
};

class SolutionDP {
  public:
    static long long maximumSum(const std::vector<int>& nums, size_t m,
                                size_t l, size_t r) {
        const size_t n = nums.size();
        // TODO: why n+2 instead of n+1 ?
        std::vector<std::vector<long long>> dp(
            n + 2, std::vector<long long>(m + 1, 0));
        std::vector<std::vector<bool>> reachable(
            n + 2, std::vector<bool>(m + 1, false));

        for (size_t i = 0; i <= n + 1; ++i)
            reachable[i][0] = true;

        // O(n * m * (r - l) * k) ≈ O(n^3) worst case
        auto get_max_subarray = [&](size_t i, size_t j, long long& sum) {
            auto valid = false;
            for (size_t k = l; k <= r; ++k) {
                if (i + k > n) break;
                if (!reachable[i + k][j - 1]) continue;
                const auto next = std::accumulate(nums.begin() + i,
                                                  nums.begin() + i + k, 0LL) +
                                  dp[i + k][j - 1];
                if (!valid || sum < next) sum = next;
                valid = true;
            }
            return valid;
        };

        auto get_max = [](std::pair<long long, bool> first,
                          std::pair<long long, bool> second)
            -> std::pair<long long, bool> {
            if (!first.second) return second;
            if (!second.second) return first;
            return {std::max(first.first, second.first), true};
        };

        for (int i = (int)n - l; i >= 0; --i)
            for (size_t j = 1; j <= m; ++j) {
                auto sum = static_cast<long long>(0);
                auto valid = get_max_subarray(i, j, sum);
                auto result =
                    get_max({sum, valid}, {dp[i + 1][j], reachable[i + 1][j]});
                if (result.second) {
                    dp[i][j] = result.first;
                    reachable[i][j] = true;
                }
            }

        auto get_max_by_subarrays_count = [&]() {
            auto valid = false;
            auto best = static_cast<long long>(0);
            for (size_t j = 1; j <= m; ++j) {
                if (!reachable[0][j]) continue;
                if (!valid || best < dp[0][j]) best = dp[0][j];
                valid = true;
            }
            return best;
        };

        return get_max_by_subarrays_count();
    }
};
