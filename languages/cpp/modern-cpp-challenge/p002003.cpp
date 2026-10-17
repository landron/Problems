/*
    2. Greatest common divisor                  p.46/428
    3. Least common multiple (of more numbers)  p.47/428

    Learnt: constexpr, std::accumulate
*/
#include <numeric>

// vcpkg providing gtest => #include <gtest/gtest.h> is the right choice.
#include <gtest/gtest.h>

#include "problems.h"

static constexpr unsigned get_greatest_common_divisor(unsigned a, unsigned b) {
    if (a < b)
        // std::swap(a, b); not constexpr
        return get_greatest_common_divisor(b, a);
    unsigned reminder = 1;
    for (reminder = a % b; reminder; a = b, b = reminder, reminder = a % b)
        ;
    return b;
}

static constexpr unsigned get_least_common_multiple(unsigned a, unsigned b) {
    const auto gcd = get_greatest_common_divisor(a, b);
    return a * b / gcd;
}

static
    /*constexpr*/ unsigned
    get_least_common_multiple(const std::vector<unsigned>& v) {
    assert(!v.empty());

    unsigned lcm = 1;
    for (auto i : v)
        lcm = get_least_common_multiple(lcm, i);
    return lcm;
}

// constexpr  //constexpr must be inline
unsigned modern_cpp_challenge::get_greatest_common_divisor(unsigned a,
                                                           unsigned b) {
    return ::get_greatest_common_divisor(a, b);
}

/*
    the correct (preferred)  solution: use accumulate
*/
unsigned modern_cpp_challenge::get_least_common_multiple(
    const std::vector<unsigned>& v) {
    const auto first = v.begin();
    const auto last = v.end();

    //  ambiguity problem
    // return std::accumulate(first, last, 1, ::get_least_common_multiple);
    return std::accumulate(first, last, 1, [](unsigned a, unsigned b) {
        return ::get_least_common_multiple(a, b);
    });
}

TEST(test_p02, main) {
    ASSERT_TRUE(2 == get_greatest_common_divisor(4, 2));
    ASSERT_TRUE(3 == get_greatest_common_divisor(9, 12));
    ASSERT_TRUE(6 == get_greatest_common_divisor(48, 54));
    ASSERT_TRUE(8 == get_greatest_common_divisor(48, 56));
    ASSERT_TRUE(12 == get_greatest_common_divisor(48, 36));
    ASSERT_TRUE(4 == get_greatest_common_divisor(4, 4));
    ASSERT_TRUE(1 == get_greatest_common_divisor(4, 3));

    static_assert(6 == get_greatest_common_divisor(48, 54));
    static_assert(18 == get_greatest_common_divisor(108, 90));
}

TEST(test_p03, main) {
    static_assert(144 == get_least_common_multiple(48, 36));
    static_assert(6 * 56 == get_least_common_multiple(48, 56));
    static_assert(7 * 144 == get_least_common_multiple(144, 56));

    ASSERT_TRUE(7 * 144 == get_least_common_multiple({12, 56, 36, 48}));
    ASSERT_TRUE(24 == get_least_common_multiple({1, 2, 8, 3}));
    ASSERT_TRUE(252 == get_least_common_multiple({2, 7, 3, 9, 4}));

    ASSERT_TRUE(7 * 144 == modern_cpp_challenge::get_least_common_multiple(
                               {12, 56, 36, 48}));
    ASSERT_TRUE(24 ==
                modern_cpp_challenge::get_least_common_multiple({1, 2, 8, 3}));
    ASSERT_TRUE(252 == modern_cpp_challenge::get_least_common_multiple(
                           {2, 7, 3, 9, 4}));
}
