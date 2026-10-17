/*
    8. Armstrong numbers
    Write a program that prints all Armstrong numbers with three digits

        List of narcissistic numbers: https://oeis.org/A005188
*/
#include "problems.h"
#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <cmath>
#include <vector>

namespace {

auto get_number_of_digits(unsigned number) {
    assert(number);

    unsigned digits = 0;
    for (; number; ++digits, number /= 10)
        ;
    return digits;
}

static inline auto powu(unsigned base, unsigned exp) {
    return static_cast<unsigned>(std::pow(base, exp));
}

/*
    In number theory, a narcissistic number, in a given number base b is a
   number that is the sum of its own digits each raised to the power of the
   number of digits.
*/
bool is_narcissistic(unsigned number, unsigned digits = 0) {
    if (digits == 0) digits = get_number_of_digits(number);

    unsigned sum = 0;
    for (unsigned i = number; i; i /= 10)
        sum += powu(i % 10, digits);
    return sum == number;
}

//  modulo, division are more expensive than multiplication and adition
void print_narcissistic_numbers_until(unsigned limit) {
    assert(limit > 10 && limit < 100000);

    unsigned i;
    for (i = 0; i < 10; ++i)
        std::cout << i << ", ";
    auto last = 0;
    for (unsigned digits = 1; i < limit; ++i) {
        switch (i) {
        case 10:
        case 100:
        case 1000:
        case 10000:
            ++digits;
        };
        if (is_narcissistic(i, digits)) {
            if (last) std::cout << last << ", ";
            last = i;
        }
    }
    if (last) std::cout << last << std::endl;
}

//  modulo, division are more expensive than multiplication and adition
void get_narcissistic_numbers_directly(unsigned no_of_digits,
                                       void (*callback)(unsigned, bool, void*),
                                       void* param) {
    assert(no_of_digits);

    for (unsigned i = no_of_digits == 1 ? 0 : powu(10, no_of_digits - 1),
                  end = powu(10, no_of_digits);
         i < end; ++i) {
        if (is_narcissistic(i, no_of_digits)) callback(i, false, param);
    }
    callback(0, true, param);
}

void get_narcissistic_numbers_generating_1(unsigned no_of_digits,
                                           void (*callback)(unsigned, bool,
                                                            void*),
                                           void* param) {
    assert(no_of_digits);

    std::vector<unsigned> digits;
    digits.resize(no_of_digits);

    digits[0] = 1;
    int current = no_of_digits - 1;
    while (current >= 0) {
        ++digits[current];
        if (digits[current] == 10) {
            digits[current] = 0;
            --current;
            continue;
        } else if (current != no_of_digits - 1) current = no_of_digits - 1;

        auto number = 0;
        auto sum = 0;
        for (unsigned i = 0; i < no_of_digits; ++i) {
            number = number * 10 + digits[i];
            sum += powu(digits[i], no_of_digits);
        }
        if (number == sum) callback(number, false, param);
    }
    callback(0, true, param);
}

void get_narcissistic_numbers_generating_2(unsigned no_of_digits,
                                           void (*callback)(unsigned, bool,
                                                            void*),
                                           void* param) {
    assert(no_of_digits);

    std::vector<unsigned> digits;
    digits.resize(no_of_digits);

    digits[0] = 1;
    auto number = powu(10, no_of_digits - 1);
    auto sum = powu(1, no_of_digits);
    for (int i = no_of_digits - 1; i >= 0;) {
        sum -= powu(digits[i], no_of_digits);
        number -= digits[i] * powu(10, no_of_digits - 1 - i);
        ++digits[i];
        if (digits[i] == 10) {
            digits[i] = 0;
            --i;
            continue;
        } else {
            sum += powu(digits[i], no_of_digits);
            number += digits[i] * powu(10, no_of_digits - 1 - i);
            if (i != no_of_digits - 1) i = no_of_digits - 1;
        }

        if (number == sum) callback(number, false, param);
    }
    callback(0, true, param);
}

void get_narcissistic_numbers_generating(unsigned no_of_digits,
                                         void (*callback)(unsigned, bool,
                                                          void*),
                                         void* param) {
    return get_narcissistic_numbers_generating_2(no_of_digits, callback, param);
}

}; // namespace

/*
    Performance
        8:  24678050, 24678051, 88593477
        https://oeis.org/A005188

    Ubuntu (ms)
            directly    generating
    6:      134         130
    7:      1536        1451
    8:      17475       19800

    Windows (ms)
            directly    generating      generating2
    7:      6329        22304           8827
    8:      79588       247596          77403

    see performance_narcissistic_numbers_* tests below
*/
void modern_cpp_challenge::print_narcissistic_numbers(unsigned limit,
                                                      unsigned generate) {
    auto print = [](unsigned number, bool is_last, void* param) {
        auto last = static_cast<unsigned*>(param);
        if (!is_last) {
            if (*last) std::cout << *last << ", " << std::flush;
            ;
            *last = number;
        } else if (*last) std::cout << *last << std::endl;
    };

    std::cout << "Printing narcisstic numbers with " << limit
              << " digits ...\n";
    std::cout << "\t(using " << (generate ? "generating" : "direct")
              << " method)" << std::endl;

    unsigned last = 0;
    switch (generate) {
    case NARCISSISTIC_DIRECT:
        get_narcissistic_numbers_directly(limit, print, &last);
        break;
    case NARCISSISTIC_GENERATE_OLD:
        get_narcissistic_numbers_generating_1(limit, print, &last);
        break;
    case NARCISSISTIC_GENERATE:
        get_narcissistic_numbers_generating_2(limit, print, &last);
        break;
    }
}

TEST(test_p8, base) {
    ASSERT_EQ(1, get_number_of_digits(6));
    ASSERT_EQ(4, get_number_of_digits(1010));

    ASSERT_TRUE(is_narcissistic(8));
    ASSERT_FALSE(is_narcissistic(11));
    ASSERT_TRUE(is_narcissistic(153));
    ASSERT_FALSE(is_narcissistic(152));
}

TEST(test_p8, 3digits_narcissistic) {
    const auto populate = [](unsigned number, bool is_last, void* param) {
        auto& numbers = *static_cast<std::vector<unsigned>*>(param);
        if (!is_last) numbers.push_back(number);
    };

    const std::vector<unsigned> expected = {153, 370, 371, 407};

    std::vector<unsigned> found;
    get_narcissistic_numbers_directly(3, populate, &found);
    ASSERT_THAT(expected, testing::ContainerEq(found));

    found.clear();
    get_narcissistic_numbers_generating(3, populate, &found);
    ASSERT_THAT(expected, testing::ContainerEq(found));
}

// 2ms
TEST(test_p8, 4digits_narcissistic) {
    const auto populate = [](unsigned number, bool is_last, void* param) {
        auto& numbers = *static_cast<std::vector<unsigned>*>(param);
        if (!is_last) numbers.push_back(number);
    };

    const std::vector<unsigned> expected = {1634, 8208, 9474};

    std::vector<unsigned> found;
    get_narcissistic_numbers_directly(4, populate, &found);
    ASSERT_THAT(expected, testing::ContainerEq(found));

    found.clear();
    get_narcissistic_numbers_generating(4, populate, &found);
    ASSERT_THAT(expected, testing::ContainerEq(found));
}

/*
    ./modern-cpp-challenge --gtest_filter=*performance_narcissistic_numbers*

    8:  24678050, 24678051, 88593477
        https://oeis.org/A005188

    Ubuntu home (ms)
            direct          generate    generate2
    7:      4447 ms         4891
    8:      50538           56462
            51149           57409       20107       2022.06

    Windows 7  (ms)
    8:      81673 ms        245143      107017
            72174           246997      86742
*/
TEST(test_p8, DISABLED_performance_narcissistic_numbers_direct) {
    using namespace modern_cpp_challenge;
    print_narcissistic_numbers(8, NARCISSISTIC_DIRECT);
}

TEST(test_p8, DISABLED_performance_narcissistic_numbers_generate) {
    using namespace modern_cpp_challenge;
    print_narcissistic_numbers(8, NARCISSISTIC_GENERATE_OLD);
}

TEST(test_p8, DISABLED_performance_narcissistic_numbers_generate_2) {
    using namespace modern_cpp_challenge;
    print_narcissistic_numbers(8, NARCISSISTIC_GENERATE);
}
