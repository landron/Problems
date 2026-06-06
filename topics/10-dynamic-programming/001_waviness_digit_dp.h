/*
https://leetcode.com/problems/total-waviness-of-numbers-in-range-ii

Digit DP (Dynamic Programming) or a Digit Trie Cache.
    [A,B] = solve([0,B]) - solve([0,A-1])
    Digit DP over numbers with a finite automaton tracking slope changes

    I had the idea, but not:
    * [A,B] = solve([0,B]) - solve([0,A-1]) - instead [A, main digit change],
    tight (see later) intervals, [last main digit change, B]
    * also, I didn't clearly see the cache on digits

#algo_digit_dp
#dp_state_machine
#pattern_digit_dp_tight             We build numbers digit-by-digit while
        respecting an upper bound using a tight constraint.
#algo_peak_valley_detection #algo_sequence_trends
#tech_state_encoding
#perf_logarithmic_digits
*/
#pragma once

/*
    Knowledge base
     * We don't cache 'is_tight = true' because those paths are unique and rare.
     * 1 <= num1 <= num2 <= 10**15​​​​​​​
*/

#include <cstring>

namespace waviness {

enum class Trend {
    // no previous direction yet: fewer than 2 effective digits or flat
    NONE = 0,
    RISING = 1,
    FALLING = 2,
    // FLAT = 3
};

struct Node {
    long long count;
    long long waves;
};

/*
position in number  : max 10**15​​​​​​​ ; 20 covers uint64_t
/ previous digit    : 10 is no previous digit
/ trend
/ started
*/
struct Cache {
    Node memo[16][11][3][2];
    bool seen[16][11][3][2];
};

Node dfs(const std::string& digits, int pos, int prev_digit, Trend trend,
         bool started, bool tight, Cache& cache) {
    /*
        DFS = Depth-First Search.

        pos        : current digit index (0 = most significant digit)
        prev_digit : previous chosen digit (10 = no digit chosen yet)
        trend      : current direction of movement (NONE / RISING / FALLING)
        started    : whether we have placed a non-leading-zero digit yet
        tight      : whether current prefix is still equal to upper bound prefix

        D = number of digits = ⌊log10(n)⌋ + 1

        Time: O(D) = O(log n), but treated as O(1) for bounded integers
            O(  (16 × 11 × 3 × 2) memo calculation
                x 10 for 0..9
                x 2 tight
            O(20 × 10 × 264) ≈ 50k operations max
        Space: O(D), treated as O(1)
            O(16 × 11 × 3 × 2) * 17 (bool + 2 * long long)
            ~1320 × 16 bytes ≈ ~21 KB
    */

    if (pos == static_cast<int>(digits.size())) return {1, 0};

    if (!tight) {
        const auto trendi = static_cast<int>(trend);
        if (cache.seen[pos][prev_digit][trendi][started])
            return cache.memo[pos][prev_digit][trendi][started];
    }

    const int limit = tight ? (digits[pos] - '0') : 9;

    Node result{0, 0};

    for (int digit = 0; digit <= limit; ++digit) {
        const auto next_tight = tight && (digit == limit);

        // Still in leading zeros
        if (!started && digit == 0) {
            auto child =
                dfs(digits, pos + 1, 10, Trend::NONE, false, next_tight, cache);

            result.count += child.count;
            result.waves += child.waves;
            continue;
        }

        int next_prev = digit;
        auto next_trend = trend;
        auto wave = false;

        if (!started) {
            // First real digit
            next_trend = Trend::NONE;
        } else if (digit > prev_digit) {
            wave = (trend == Trend::FALLING);
            next_trend = Trend::RISING;
        } else if (digit < prev_digit) {
            wave = (trend == Trend::RISING);
            next_trend = Trend::FALLING;
        } else
            // next_trend = Trend::FLAT;
            next_trend = Trend::NONE;

        auto child = dfs(digits, pos + 1, next_prev, next_trend, true,
                         next_tight, cache);

        result.count += child.count;

        // waves below
        result.waves += child.waves;

        // newly created wave applies to every completion
        result.waves += wave * child.count;
    }

    if (!tight) {
        const auto trendi = static_cast<int>(trend);
        cache.seen[pos][prev_digit][trendi][started] = true;
        cache.memo[pos][prev_digit][trendi][started] = result;
    }

    return result;
}

template <std::integral T>
[[nodiscard]] constexpr T waviness_dp(T a, T b) {
    assert(a <= b);

    // Lambda helper to cleanly isolate the DP run and its cache reset
    auto solve = [](T n) -> T {
        if (n < 100) return 0; // Peaks/valleys require at least 3 digits

        Cache cache;
        std::memset(cache.seen, 0, sizeof(cache.seen));

        auto res = dfs(std::to_string(n), 0,
                       10,          // no previous digit
                       Trend::NONE, // flat/start
                       false, true, cache
                    );

        return res.waves;
    };

    // Safely handle lower bound edge case when a is 0
    T result_b = solve(b);
    T result_a = (a > 0) ? solve(a - 1) : 0;

    return result_b - result_a;
}

class SolutionDigitDP {
    // ChatGPT base solution
  public:
    template <std::integral T>
    [[nodiscard]] static constexpr T totalWaviness(T num1, T num2) noexcept {
        return waviness_dp(num1, num2);
    }
};

} // namespace waviness
