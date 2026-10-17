/*
    9. Prime factors of a number
*/

#include "math.h"
#include "problems.h"
#include <gmock/gmock.h>
#include <gtest/gtest.h>

void modern_cpp_challenge::print_prime_factors(unsigned long long number) {
    using namespace math_lib;

    const auto primes = get_primes_for(number);
    const auto divisors = get_prime_divisors(number, primes);

    auto print_b = [](Number divisor, unsigned power, bool is_last) {
        if (power != 1) std::cout << divisor << "^" << power;
        else std::cout << divisor;
        if (!is_last) std::cout << " * ";
    };

    auto print = [print_b](const Divisor& divisor, bool is_last = false) {
        print_b(std::get<0>(divisor), std::get<1>(divisor), is_last);
    };

    std::cout << number << " = ";
    for (size_t i = 0; i < divisors.size() - 1; ++i)
        print(divisors[i]);
    print(divisors.back(), true);
    std::cout << std::endl;
}

/*
    ./modern-cpp-challenge --gtest_filter=*largest_prime_factor*
    264ms

    As a further exercise, determine the largest prime factor for the number
   600,851,475,143. 6857
*/
TEST(test_p9, DISABLED_largest_prime_factor) {
    static_assert(sizeof(unsigned long) >= 4);
    static_assert(1llu * 71 * 839 * 1471 * 6857 == 600'851'475'143);
    modern_cpp_challenge::print_prime_factors(600'851'475'143);
}
