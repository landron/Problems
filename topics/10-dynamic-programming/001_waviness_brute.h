/*
https://leetcode.com/problems/total-waviness-of-numbers-in-range-i
    Not enough for https://leetcode.com/problems/total-waviness-of-numbers-in-range-ii
*/
#pragma once

#include <format>
#include <print>
#include <ranges>
#include <version>

namespace waviness {

class SolutionBrute {
  public:
    SolutionBrute() : start(std::time(nullptr)) {}

    template <std::integral T>
    [[nodiscard]] constexpr T totalWaviness(T num1, T num2) const /*noexcept*/ {
        /*
        num2 == std::numeric_limits<T>::max() fails
        */
        T waviness = 0;
        if (num1 == 0) ++num1;
        for (auto i : std::views::iota(num1, num2)) {
            waviness += wavinessFor(i);

            constexpr unsigned period = 1'000'000;
            if (i % period == 0) {
                std::print("{}\n", i / period);
                constexpr unsigned wait = 4;
                if (std::difftime(std::time(nullptr), start) > wait)
                    throw_timeout_exception(wait);
            }
        }
        waviness += wavinessFor(num2);

        return waviness;
    }

  private:
    template <std::integral T>
    [[nodiscard]] constexpr T wavinessFor(T num) const noexcept {
        if (num < 100) return 0;

        auto right = num % 10;
        num /= 10;
        auto middle = num % 10;
        num /= 10;

        T waviness = 0;
        for (auto left = num % 10; num > 0;
             num /= 10, right = middle, middle = left, left = num % 10) {
            // cout << right << "," << middle << "," << left << "\n";
            if (right < middle) {
                if (middle > left) ++waviness;
            } else if (right > middle) {
                if (middle < left) ++waviness;
            }
        }

        return waviness;
    }

    inline void throw_timeout_exception(unsigned wait) const {
        static_assert(202603L == __cpp_lib_format);

#if defined(__cpp_lib_format) &&                                               \
    __cpp_lib_format >= 202609L // Fictional/Target C++26 date for _cf
        // Use the cutting-edge C++26 native formatting if available
        using namespace std::literals;
        throw std::runtime_error("Timeout: More than {} seconds elapsed."_cf,
                                 wait);
#else
        // Safe fallback for GCC 16 and older C++20/C++23 compilers
        throw std::runtime_error(
            std::format("Timeout: More than {} seconds elapsed.", wait));
#endif
    }

  private:
    const time_t start;
};

} // namespace waviness
