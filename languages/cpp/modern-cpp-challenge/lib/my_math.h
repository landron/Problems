// Not math.h: avoid conflict with the C standard library header
#pragma once

#include <cmath>
#include <utility>
#include <vector>

namespace math_lib {

using Number = unsigned long long;
using Primes = std::vector<Number>;
using Divisor = std::pair<Number, unsigned>;
using Divisors = std::vector<Divisor>;
using ProperDivisors = Primes;

Primes get_primes(unsigned long long);
static Primes get_primes_for(unsigned long long);
Divisors get_prime_divisors(unsigned long long, const Primes& primes);

// This is still slow
ProperDivisors get_proper_divisors(const Divisors& prime_divisors);
} // namespace math_lib

static math_lib::Primes math_lib::get_primes_for(Number number) {
    const auto primes_limit = 1 + std::floor(std::sqrt(number));
    // double -> integer
    return get_primes(static_cast<Number>(primes_limit));
}
