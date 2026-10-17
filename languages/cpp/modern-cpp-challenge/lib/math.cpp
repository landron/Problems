#include "my_math.h"

#include "utils.h"

#include <algorithm>
#include <cassert>
#include <cmath>
#include <gtest/gtest.h>
#include <set>
#include <vector>

using namespace math_lib;

/*
    Reference
        proj_euler.py/get_primes_2

    Return value
        no cost: the vector will be just moved
*/
Primes math_lib::get_primes(unsigned long long limit) {
    if (limit < 3) return {};

    Primes primes;

    std::vector<unsigned> sieve_of_Eratosthenes;
    sieve_of_Eratosthenes.resize(limit / 2);
    for (auto i = 0; i < sieve_of_Eratosthenes.size() - 1; ++i)
        sieve_of_Eratosthenes[i] = i * 2 + 3;
    auto& sieve = sieve_of_Eratosthenes;

    const auto limit_of_sieve = 1 + std::floor(std::sqrt(limit));
    for (size_t i = 3; i < limit_of_sieve; i += 2)
        if (sieve[i / 2 - 1])
            for (size_t j = i * i; j < limit; j += 2 * i)
                sieve[j / 2 - 1] = 0;

    primes.push_back(2);
    for (auto i = 0; i < sieve.size(); ++i)
        if (sieve[i]) primes.push_back(sieve[i]);

    return primes;
}

/*
    Reference
        proj_euler.py/get_prime_divisors
*/
Divisors math_lib::get_prime_divisors(unsigned long long number,
                                      const Primes& primes) {
    const auto get_power = [](auto& number, auto divisor) {
        using NumberType = std::remove_reference<decltype(number)>::type;

        assert(number % divisor == 0);
        NumberType power{};
        while (number % divisor == 0) {
            power += 1;
            number /= divisor;
        }
        return power;
    };

    Divisors divisors;
    const auto limit = 1 + static_cast<unsigned>(std::floor(std::sqrt(number)));
    for (auto i : primes) {
        if (limit < i) break;
        if (number % i) continue;
        divisors.push_back(
            std::make_pair(i, static_cast<unsigned>(get_power(number, i))));
        if (number == 1) break;
    }
    if (number != 1) divisors.push_back(std::make_pair(number, 1));

    return divisors;
}

/*
    Purpose
        this is slow, see print_amicable_numbers_advanced
            performance: math_performance.get_proper_divisors_recursively
        get_proper_divisors_iteratively is better, but not enough

    tag_recursive_lambda
    #recursive_lambda
        https://stackoverflow.com/questions/2067988/recursive-lambda-functions-in-c11

    TODO: is set really needed here ? I do not think is possible to find the
   same number multiple times
*/
static ProperDivisors
    get_proper_divisors_recursively(const Divisors& prime_divisors) {
    assert(!prime_divisors.empty());
    // std::cout << "get_proper_divisors: " << utils::to_string(prime_divisors)
    // << std::endl;

    using AllDivisors = std::set<Primes::value_type>;

    // std::function<auto(auto,const Divisors&, size_t, auto, AllDivisors&)
    // get_all_combinations;
    const auto get_all_combinations = [](const Divisors& prime_divisors,
                                         size_t where, auto current,
                                         AllDivisors& result) {
        const auto get_all_combinations_impl =
            [](const Divisors& prime_divisors, size_t where, auto current,
               AllDivisors& result, auto& get_all_combinations_func) -> void {
            using NumberType = std::remove_reference<decltype(current)>::type;

            // 0 = without
            for (NumberType i = 0, factor = 1;
                 i <= prime_divisors[where].second;
                 ++i, factor *= prime_divisors[where].first) {
                const auto next = current * factor;
                // std::cout << "get_all_combinations: " << current << "," <<
                // factor << std::endl;
                result.insert(next);
                if (where + 1 < prime_divisors.size())
                    get_all_combinations_func(prime_divisors, where + 1, next,
                                              result,
                                              get_all_combinations_func);
            }
        };

        return get_all_combinations_impl(prime_divisors, where, current, result,
                                         get_all_combinations_impl);
    };

    AllDivisors result{1};
    get_all_combinations(prime_divisors, 0llu, 1llu, result);
    ProperDivisors divisors;
    for (auto i : result) {
        // std::cout << i << " ";
        divisors.push_back(i);
    }
    // not the number itself
    divisors.pop_back();
    // std::cout << std::endl;
    return divisors;
}

/*
    Purpose
        two times better than the recursive verion
            math_performance.get_proper_divisors_iteratively
        BUT not enough (the direct version is 10x better for 1M numbers)

    Parameters
        Ex.: (2,3), (3,1), (5,1), (7,2)
*/
static ProperDivisors
    get_proper_divisors_iteratively(const Divisors& prime_divisors) {
    assert(!prime_divisors.empty());

    //  iterate the cartesian product of the given primes
    std::vector<size_t> iterators;
    iterators.resize(prime_divisors.size());

    const auto get_product = [](const Divisors& primes,
                                const std::vector<size_t>& iterators) {
        double prod = 1;
        for (size_t i = 0; i < iterators.size(); ++i)
            prod *= std::pow(primes[i].first, iterators[i]);
        return prod;
    };

    const auto get_next = [](const Divisors& primes,
                             std::vector<size_t>& iterators) {
        for (auto pos = 0; pos < iterators.size(); ++pos) {
            if (iterators[pos] < primes[pos].second) {
                ++iterators[pos];
                return true;
            }
            iterators[pos] = 0;
        };
        return false;
    };

    ProperDivisors divisors;
    do {
        // std::cout << utils::to_string(iterators) << std::endl;

        const auto next_divisor = get_product(prime_divisors, iterators);
        divisors.push_back(
            static_cast<ProperDivisors::value_type>(next_divisor));
    } while (get_next(prime_divisors, iterators));

    //  O(NlogN): this is dominated by the previous loop
    std::sort(divisors.begin(), divisors.end());
    divisors.pop_back();

    return divisors;
}

ProperDivisors math_lib::get_proper_divisors(const Divisors& prime_divisors) {
    // return get_proper_divisors_recursively(prime_divisors);
    return get_proper_divisors_iteratively(prime_divisors);
}

TEST(math, get_primes) {
    using namespace math_lib;

    ASSERT_EQ(Primes({}), get_primes(2));
    ASSERT_EQ(Primes({2, 3}), get_primes(5));
    ASSERT_EQ(Primes({2, 3, 5, 7}), get_primes(10));
    ASSERT_EQ(25, get_primes(100).size());

    if (0)
        std::cout << "get_primes(5) " << get_primes(100).size() << "."
                  << std::endl;
}

TEST(math, get_prime_divisors) {
    using namespace math_lib;

    const auto primes_1000 = get_primes(1000);
    ASSERT_EQ((Divisors{{2u, 2u}}), get_prime_divisors(4, primes_1000));
    ASSERT_EQ((Divisors{{5u, 1u}}), get_prime_divisors(5, primes_1000));
    ASSERT_EQ((Divisors{{2u, 1u}, {3u, 1u}}),
              get_prime_divisors(6, primes_1000));
    ASSERT_EQ((Divisors{{2u, 3u}}), get_prime_divisors(8, primes_1000));
    ASSERT_EQ((Divisors{{2u, 2u}, {7u, 1u}}),
              get_prime_divisors(28, primes_1000));
    ASSERT_EQ((Divisors{{2u, 3u}, {7u, 1u}}),
              get_prime_divisors(56, primes_1000));
    ASSERT_EQ((Divisors{{2u, 3u}, {3u, 2u}}),
              get_prime_divisors(72, primes_1000));

    /*    std::cout << "get_prime_divisors(100) "
                  << utils::to_string(get_prime_divisors(100, primes_1000)) <<
       "." << std::endl;*/
}

/*
    modern-cpp-challenge.exe --gtest_filter=math.get_proper_divisors
*/
TEST(math, get_proper_divisors) {
    using namespace math_lib;
    using Divs = Primes;

    const auto primes_1000 = get_primes(1000);

    auto prime_divisors = get_prime_divisors(2, primes_1000);
    ASSERT_EQ(Divs({1}), get_proper_divisors_recursively(prime_divisors));
    ASSERT_EQ(Divs({1}), get_proper_divisors_iteratively(prime_divisors));

    prime_divisors = get_prime_divisors(6, primes_1000);
    ASSERT_EQ(Divs({1, 2, 3}), get_proper_divisors_iteratively(prime_divisors));
    ASSERT_EQ(Divs({1, 2, 3}), get_proper_divisors_recursively(prime_divisors));

    prime_divisors = get_prime_divisors(8, primes_1000);
    ASSERT_EQ(Divs({1, 2, 4}), get_proper_divisors_iteratively(prime_divisors));
    ASSERT_EQ(Divs({1, 2, 4}), get_proper_divisors_recursively(prime_divisors));

    prime_divisors = get_prime_divisors(12, primes_1000);
    ASSERT_EQ(Divs({1, 2, 3, 4, 6}),
              get_proper_divisors_iteratively(prime_divisors));
    ASSERT_EQ(Divs({1, 2, 3, 4, 6}),
              get_proper_divisors_recursively(prime_divisors));

    prime_divisors = get_prime_divisors(24, primes_1000);
    ASSERT_EQ(Divs({1, 2, 3, 4, 6, 8, 12}),
              get_proper_divisors_iteratively(prime_divisors));
    ASSERT_EQ(Divs({1, 2, 3, 4, 6, 8, 12}),
              get_proper_divisors_recursively(prime_divisors));

    prime_divisors = get_prime_divisors(8 * 3 * 5 * 49, primes_1000);
    ASSERT_EQ(get_proper_divisors_recursively(prime_divisors),
              get_proper_divisors_iteratively(prime_divisors));
}

/*
    modern-cpp-challenge.exe
   --gtest_filter=math_performance.get_proper_divisors_recursively

    10000:      0.565s
    100000:     5.742s
*/
TEST(math_performance, DISABLED_get_proper_divisors_recursively) {
    const auto primes_1000 = get_primes(1000);
    const auto divisors = get_prime_divisors(24, primes_1000);
    for (auto i = 0; i < 10000; ++i)
        ASSERT_EQ(Primes({1, 2, 3, 4, 6, 8, 12}),
                  get_proper_divisors_recursively(divisors));
}

/*
    modern-cpp-challenge.exe
   --gtest_filter=math_performance.get_proper_divisors_iteratively

    10000:      0.379s
    100000:     3.877s
*/
TEST(math_performance, DISABLED_get_proper_divisors_iteratively) {
    const auto primes_1000 = get_primes(1000);
    const auto divisors = get_prime_divisors(24, primes_1000);
    for (auto i = 0; i < 10000; ++i)
        ASSERT_EQ(Primes({1, 2, 3, 4, 6, 8, 12}),
                  get_proper_divisors_iteratively(divisors));
}

/*
    100000:     3.587s
*/
TEST(math_performance, DISABLED_get_proper_divisors_iteratively_no_sort) {
    const auto primes_1000 = get_primes(1000);
    const auto divisors = get_prime_divisors(24, primes_1000);
    for (auto i = 0; i < 100000; ++i)
        ASSERT_EQ(Primes({1, 2, 4, 8, 3, 6, 12}),
                  get_proper_divisors_iteratively(divisors));
}
