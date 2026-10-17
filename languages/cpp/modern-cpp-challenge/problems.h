#pragma once

#include "lib/my_math.h"

namespace modern_cpp_challenge {
using BigInteger = unsigned long long;

BigInteger sum_of_divisible_3_5(unsigned limit);
/*constexpr*/ unsigned get_greatest_common_divisor(unsigned, unsigned);
unsigned get_least_common_multiple(const std::vector<unsigned>&);

unsigned get_abundance(unsigned, const math_lib::Primes&);
void print_abundant_numbers(unsigned limit);
void print_amicable_numbers(unsigned limit);
enum {
    NARCISSISTIC_DIRECT,
    NARCISSISTIC_GENERATE_OLD,
    NARCISSISTIC_GENERATE,
};
void print_narcissistic_numbers(unsigned limit, unsigned generate);
void print_prime_factors(unsigned long long number);
void print_gray_code_until(unsigned number);
}; // namespace modern_cpp_challenge
