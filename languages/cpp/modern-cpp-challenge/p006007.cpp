/*
    p6 Abundant numbers
        The direct solution (find the divisors by trying all the smaller
   numbers) is much simpler, but less C++ enriching.

    p7 Amicable numbers

    TODO
        * see modern_cpp_challenge::print_amicable_numbers
            improve the "advanced" variant performance: generating divisors from
   prime factors is slow
*/
#include "lib/utils.h"
#include "problems.h"
#include <gtest/gtest.h>

#include <cmath>
#include <iostream>
#include <numeric>

namespace {

template <typename NumberType>
inline auto proper_divisors_sum(NumberType number) {
    const auto limit =
        1 + static_cast<NumberType>(std::floor(std::sqrt(number)));
    decltype(number) sum = 1;
    for (decltype(number) i = 2; i < limit; ++i) {
        if (number % i == 0) {
            sum += i;
            const auto other = static_cast<NumberType>(number / i);
            // skip the other 2 for 4
            if (other != i) sum += other;
        }
    }
    return sum;
}

template <typename NumberType>
inline auto advanced_proper_divisors_sum(NumberType number,
                                         const math_lib::Primes& primes) {
    const auto prime_divs = math_lib::get_prime_divisors(number, primes);
    if (prime_divs.empty())
        std::cout << "prime_divs.empty(): " << number << std::endl;

    const auto divs = math_lib::get_proper_divisors(prime_divs);
    return std::accumulate(divs.begin(), divs.end(), 0llu);
}

/*
    Performance
        * proper_divisors_sum
            1000000: 4.3s
*/
void print_amicable_numbers_direct(unsigned limit) {
    for (decltype(limit) i = 2; i < limit; ++i) {
        const auto sum = proper_divisors_sum(i);
        if (sum > i && sum < limit && i == proper_divisors_sum(sum))
            std::cout << "(" << i << "," << sum << ")" << std::endl;
    }
}

/*
    Performance
        * advanced_proper_divisors_sum
            1000000: 116.51!!!
                     92.421s with the no-recursion variant
*/
void print_amicable_numbers_advanced(unsigned limit) {
    const auto get_primes = [](auto limit) {
        const auto primes_limit =
            1 + static_cast<unsigned>(std::floor(std::sqrt(limit)));
        return math_lib::get_primes(primes_limit);
    };
    const auto primes = get_primes(limit);
    // std::cout << "print_amicable_numbers_advanced(" << limit << "): "
    //           << utils::to_string(primes) << std::endl;

    for (decltype(limit) i = 2; i < limit; ++i) {
        const auto sum = advanced_proper_divisors_sum(i, primes);
        if (sum > i && sum < limit &&
            i == advanced_proper_divisors_sum(sum, primes))
            std::cout << "(" << i << "," << sum << ")" << std::endl;
    }
}

} // anonymous namespace

unsigned modern_cpp_challenge::get_abundance(unsigned number,
                                             const math_lib::Primes& primes) {
    const auto sum =
        static_cast<unsigned>(advanced_proper_divisors_sum(number, primes));
    return sum > number ? (sum - number) : 0;
}

void modern_cpp_challenge::print_abundant_numbers(unsigned limit) {
    const auto primes = math_lib::get_primes(limit);
    for (decltype(limit) i = 2; i < limit; ++i) {
        const auto abundance = get_abundance(i, primes);
        if (abundance)
            std::cout << "(" << i << ":" << abundance << ")" << std::endl;
    }
}

/*
    generating the divisors is significantly slower than direct testing for them
*/
void modern_cpp_challenge::print_amicable_numbers(unsigned limit) {
    print_amicable_numbers_direct(limit);
    // print_amicable_numbers_advanced(limit);
}

TEST(test_p06, main) {
    using namespace modern_cpp_challenge;

    const auto primes_1000 = math_lib::get_primes(1000);
    ASSERT_EQ(4, get_abundance(12, primes_1000));
    ASSERT_EQ(0, get_abundance(16, primes_1000));
    ASSERT_EQ(3, get_abundance(18, primes_1000));
    ASSERT_EQ(2, get_abundance(20, primes_1000));
    ASSERT_EQ(12, get_abundance(24, primes_1000));
    // std::cout << get_abundance(18, primes_1000) << std::endl;
}

TEST(test_p7, proper_divisors_sum) {
    //  perfect numbers
    ASSERT_EQ(6, proper_divisors_sum(6));
    ASSERT_EQ(28, proper_divisors_sum(28));

    ASSERT_EQ(284, proper_divisors_sum(220));
    ASSERT_EQ(220, proper_divisors_sum(284));
    ASSERT_EQ(1184, proper_divisors_sum(1210));
    ASSERT_EQ(1210, proper_divisors_sum(1184));
}

/*
    modern-cpp-challenge.exe --gtest_filter=test_p7*
*/
TEST(test_p7, advanced_proper_divisors_sum) {
    const auto primes_1000 = math_lib::get_primes(1000);

    //  perfect numbers
    ASSERT_EQ(6, advanced_proper_divisors_sum(6, primes_1000));
    ASSERT_EQ(28, advanced_proper_divisors_sum(28, primes_1000));

    ASSERT_EQ(284, advanced_proper_divisors_sum(220, primes_1000));
    ASSERT_EQ(220, advanced_proper_divisors_sum(284, primes_1000));
    ASSERT_EQ(1184, advanced_proper_divisors_sum(1210, primes_1000));
    ASSERT_EQ(1210, advanced_proper_divisors_sum(1184, primes_1000));
}

TEST(test_p7, DISABLED_amicable_numbers_SLOW_two_ways) {
    static constexpr unsigned LIMIT = 30000;

    const auto get_primes = [](auto limit) {
        const auto primes_limit =
            1 + static_cast<unsigned>(std::floor(std::sqrt(limit)));
        return math_lib::get_primes(primes_limit);
    };
    const auto primes = get_primes(LIMIT);

    for (std::remove_const<decltype(LIMIT)>::type i = 2; i < LIMIT; ++i) {
        const auto sum1 = advanced_proper_divisors_sum(i, primes);
        const auto amicable1 = sum1 > i && sum1 < LIMIT &&
                               i == advanced_proper_divisors_sum(sum1, primes);
        const auto sum2 = proper_divisors_sum(i);
        const auto amicable2 =
            sum2 > i && sum2 < LIMIT && i == proper_divisors_sum(sum2);
        // std::cout << i << "," << sum1 << "," << sum2 << std::endl;

        ASSERT_EQ(sum1, sum2);
        ASSERT_EQ(amicable1, amicable2);
        if (amicable1) std::cout << "(" << i << "," << sum1 << ")" << std::endl;
    }
}
