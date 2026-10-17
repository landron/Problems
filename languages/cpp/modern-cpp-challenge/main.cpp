/*
    Next problem: p8, p52, narcissistic numbers

    TODO:
        p7, performance: generating the divisors variant is 20 times slower than
   the direct version
*/
#include <iostream>

// vcpkg providing gtest => #include <gtest/gtest.h> is the right choice.
#include <gtest/gtest.h>

#include "lib/measure.h"
#include "problems.h"

auto constexpr DO_EXECUTE = false;

using namespace modern_cpp_challenge;

/*
    filter :
        modern-cpp-challenge.exe --gtest_filter=test_main*
*/
TEST(test_main, almost_all_problems) {
    if (DO_EXECUTE) {
        (void)sum_of_divisible_3_5(100);
        (void)get_greatest_common_divisor(48, 54);

        if (0) print_abundant_numbers(200);

        if (0) {
            utils::Duration measure("print_amicable_numbers(1000000)");
            print_amicable_numbers(1000000);
        }

        if (0) print_narcissistic_numbers(8, NARCISSISTIC_GENERATE);

        if (0) print_gray_code_until(32);
    }
}
