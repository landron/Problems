"""
https://leetcode.com/problems/number-of-zigzag-arrays-i
    TODO: https://leetcode.com/problems/number-of-zigzag-arrays-ii/
            3 <= n <= 10**9, 1 <= l < r <= 75​​​​​​​
            vs
            3 <= n <= 2000, 1 <= l < r <= 2000

black, ruff check

Hint 3: Speed up with prefix/suffix sums so each layer updates in O(m) instead of O(m2)

#algo_dynamic_programming
#dp_direction_state
    State tracks whether the last step was up or down.
#dp_last_value_state
    State also tracks the last value.
#dp_prefix_sum_transition
    up[i] needs all down[j] for j < i.
    down[i] needs all up[j] for j > i.
    Prefix/suffix sums make these transitions O(1).
#dp_state_compression
    Only the previous length layer is needed.
    (DP[length] depends only on DP[length-1])
#pattern_alternating_sequence
#perf_o_nm
#perf_space_optimized_dp
"""

MOD = 10**9 + 7


def zig_zag_arrays_top_down(size, left, right):
    """
    O(n*M*M) version, where M = right - left +1: no prefix sums, insufficient
        (timeouts) for large M versions.
    """
    dp = [
        [[-1 for _ in range(right - left + 1)] for _ in range(2)] for _ in range(size)
    ]

    def recursive_step(left, right, dp, size, up, val):
        assert left <= val <= right
        assert 0 <= size

        if size == 0:
            return 1

        if dp[size - 1][up][val - left] != -1:
            return dp[size - 1][up][val - left]

        no_arrays = 0
        if up:
            for i in range(val + 1, right + 1):
                no_arrays += recursive_step(left, right, dp, size - 1, not up, i)
        else:
            for i in range(left, val):
                no_arrays += recursive_step(left, right, dp, size - 1, not up, i)

        no_arrays %= MOD
        dp[size - 1][up][val - left] = no_arrays
        return no_arrays

    no_arrays = 0
    for i in range(left, right + 1):
        no_arrays += recursive_step(left, right, dp, size - 1, True, i)
        no_arrays += recursive_step(left, right, dp, size - 1, False, i)
        no_arrays %= MOD
    return no_arrays


def zig_zag_arrays_buttom_up(size, left, right):
    """
    Computes the number of valid zigzag arrays of a given size within [left, right].

    Algorithm: Iterative DP with Prefix/Suffix Sum Optimization
    ----------------------------------------------------------
    Time Complexity: O(size * M) where M = right - left + 1.
                     Eliminates the inner loop of the top-down approach by
                     caching cumulative subarray sums for O(1) state transitions.

    Solves
        Top-down timeouts for (29, 44, 606)
    Problems
        timeout (smalls) for (2000, 2, 1999): see zig_zag_arrays_buttom_up_2
    """
    variation = right - left + 1
    assert 3 <= size
    assert 1 <= variation

    # True = up
    dp = {True: [1] * variation, False: [1] * variation}

    for _ in range(2, size + 1):
        # prefix[i] will store sum(dp[False][0] ... dp[False][i-1])
        prefix = [0] * (variation + 1)
        for i in range(variation):
            prefix[i + 1] = (prefix[i] + dp[False][i]) % MOD

        # suffix[i] will store sum(dp[True][i+1] ... dp[True][M-1])
        suffix = [0] * (variation + 1)
        for i in range(variation - 1, -1, -1):
            suffix[i] = (suffix[i + 1] + dp[True][i]) % MOD

        for i in range(variation):
            # beware of the direction swtich!

            # up trend ending at i: needs previous values strictly less than i
            dp[True][i] = prefix[i]
            # down trend ending at i: needs previous values strictly greater than i
            dp[False][i] = suffix[i + 1]
        # print(dp)

    no_arrays = sum(dp[True]) + sum(dp[False])
    no_arrays %= MOD
    return no_arrays


def zig_zag_arrays_buttom_up_2(size, left, right):
    """
    zig_zag_arrays_buttom_up + 2 optimizations (list vs dictionary, pre-allocation)
    """
    variation = right - left + 1
    assert 3 <= size
    assert 1 <= variation

    # 1. Use fast local lists instead of dictionaries
    dp_true = [1] * variation
    dp_false = [1] * variation

    # 2. Pre-allocate prefix/suffix arrays once to stop recreating them in the loop
    prefix = [0] * (variation + 1)
    suffix = [0] * (variation + 1)

    for _ in range(2, size + 1):
        # prefix[i] will store sum(dp_false[0] ... dp_false[i-1])
        for i in range(variation):
            prefix[i + 1] = (prefix[i] + dp_false[i]) % MOD

        # suffix[i] will store sum(dp_true[i+1] ... dp_true[M-1])
        for i in range(variation - 1, -1, -1):
            suffix[i] = (suffix[i + 1] + dp_true[i]) % MOD

        for i in range(variation):
            # beware of the direction swtich!

            # up trend ending at i: needs previous values strictly less than i
            dp_true[i] = prefix[i]
            # down trend ending at i: needs previous values strictly greater than i
            dp_false[i] = suffix[i + 1]
        # print(dp)

    no_arrays = sum(dp_true) + sum(dp_false)
    no_arrays %= MOD
    return no_arrays


def debug_assertions():
    """
    unit tests
    """
    assert 2 == zig_zag_arrays_top_down(3, 4, 5)
    assert 2 == zig_zag_arrays_buttom_up(3, 4, 5)
    assert 2 == zig_zag_arrays_buttom_up_2(3, 4, 5)

    assert 10 == zig_zag_arrays_top_down(3, 1, 3)
    assert 10 == zig_zag_arrays_buttom_up(3, 1, 3)
    assert 10 == zig_zag_arrays_buttom_up_2(3, 1, 3)

    # timeout (without cache)
    assert 21989242 == zig_zag_arrays_top_down(6, 13, 35)
    assert 21989242 == zig_zag_arrays_buttom_up(6, 13, 35)
    assert 21989242 == zig_zag_arrays_buttom_up_2(6, 13, 35)

    # forgotten modulo: 2650716814
    assert 650716800 == zig_zag_arrays_top_down(7, 9, 39)
    assert 650716800 == zig_zag_arrays_buttom_up(7, 9, 39)
    assert 650716800 == zig_zag_arrays_buttom_up_2(7, 9, 39)

    # too much for Top-Down
    assert 263751293 == zig_zag_arrays_buttom_up(29, 44, 606)
    assert 263751293 == zig_zag_arrays_buttom_up_2(29, 44, 606)

    # too much for zig_zag_arrays_buttom_up
    assert 110774199 == zig_zag_arrays_buttom_up_2(2000, 2, 1999)


def main():
    """Main function to run the tests."""
    # res = Solution().zigZagArrays(3, 4, 5)
    # print(res)

    debug_assertions()


if __name__ == "__main__":
    main()
