/*
        10. Print binary representation, Gray code representation

        Lessons:
        * std::bitset
        * first calculate, then think about how to display (string conversions)
        * do what the problem ask
*/
#include "math.h"
#include "problems.h"
#include <bitset>
#include <gmock/gmock.h>
#include <gtest/gtest.h>

static inline auto get_binary(unsigned number) {
    std::string binary;
    while (number > 1) {
        if (number % 2) binary += '1';
        else binary += '0';
        number /= 2;
    }
    binary += number ? '1' : '0';
    std::reverse(binary.begin(), binary.end());
    return binary;
};

//	solution
static inline std::string to_binary(unsigned int value, int const digits) {
    return std::bitset<32>(value).to_string().substr(32 - digits, digits);
}

/*
        binary reflected Gray code
                https://mathworld.wolfram.com/GrayCode.html
*/
static inline auto get_gray_code(const std::string& binary) {
    std::string gray(binary);
    for (size_t i = gray.length() - 1; i > 0; --i)
        if (gray[i - 1] == '1') gray[i] = (gray[i] == '1') ? '0' : '1';
    return gray;
};

static inline auto get_gray_code(unsigned number) {
    const auto binary = get_binary(number);
    return get_gray_code(binary);
};

/*
        https://www.tutorialspoint.com/python-program-to-convert-gray-code-to-binary
*/
static inline auto gray_decode(const std::string& gray) {
    std::string binary;
    binary.resize(gray.length());
    binary[0] = gray[0];
    for (size_t i = 1; i < gray.length(); ++i) {
        if (gray[i] == '0') binary[i] = binary[i - 1];
        else binary[i] = binary[i - 1] == '0' ? '1' : '0';
    }

    return binary;
};

static inline auto get_number(const std::string& binary) {
    unsigned number = 0;
    for (size_t i = 0; i < binary.length(); ++i) {
        number <<= 1;
        number += (binary[i] == '0' ? 0 : 1);
    }
    return number;
};

namespace solution {

inline unsigned gray_encode(unsigned number) {
    return number ^ (number >> 1);
}

unsigned gray_decode(unsigned gray) {
    for (unsigned bit = 1U << 31; bit > 1; bit >>= 1) {
        if (gray & bit) gray ^= bit >> 1;
    }
    return gray;
}

} // namespace solution

void modern_cpp_challenge::print_gray_code_until(unsigned number) {
    /*
            https://mathworld.wolfram.com/GrayCode.html
            TO-DO: there is an error
    */
    auto gray_decode_1 = [](const std::string& gray) {
        auto gray_sum = [](const std::string& gray, size_t until) {
            size_t sum = 0;
            for (auto i = 0; i <= until; ++i)
                sum += ('1' - gray[i]);
            return sum % 2 == 1;
        };
        std::string binary;
        binary.resize(gray.length());
        for (size_t i = 0; i < gray.length(); ++i) {
            const auto pos = gray.length() - 1 - i;
            binary[pos] =
                gray_sum(gray, pos) ? ('1' - gray[pos] + '0') : gray[pos];
        }
        //	std::cout << "Binary: " << binary << std::endl;

        return binary;
    };

    /*
            https://www.geeksforgeeks.org/code-converters-binary-to-from-gray-code/
            xor using formula
            TO-DO:	it does not work
    */
    auto gray_decode_2 = [](const std::string& gray) {
        auto gray_sum = [](const std::string& gray, size_t pos) {
            size_t sum = gray[gray.size() - 1];
            for (auto i = gray.size() - 1; i > pos; --i)
                sum ^= gray[i];
            return sum;
        };
        std::string binary;
        binary.resize(gray.length());
        for (size_t i = 0; i < gray.length(); ++i) {
            const auto pos = gray.length() - 1 - i;
            binary[pos] = gray_sum(gray, pos) ? '1' : '0';
        }
        // std::cout << "Binary: " << binary << std::endl;

        return binary;
    };

    // std::cout << number << std::endl;
    // const auto binary = get_binary(number);
    // std::cout << "Binary: " << binary << std::endl;
    // const auto gray = get_gray_code(binary);
    // std::cout << "Gray code: " << gray << std::endl;
    // std::cout << "Decoded: " << gray_decode(gray) << std::endl;
    // std::cout << std::endl;

    std::cout << "Number\tBinary\tGray\tDecoded\n";
    std::cout << "------\t------\t----\t-------\n";
    for (unsigned n = 0; n < 32; ++n) {
        const auto enc = solution::gray_encode(n);
        std::cout << n << "\t" << to_binary(n, 5) << "\t" << to_binary(enc, 5)
                  << "\t" << solution::gray_decode(enc) << "\n";
    }
}

TEST(test_p10, get_gray) {
    ASSERT_EQ("0", get_gray_code(0));
    ASSERT_EQ("1", get_gray_code(1));
    ASSERT_EQ("11", get_gray_code(2));
    ASSERT_EQ("10", get_gray_code(3));
    ASSERT_EQ("101", get_gray_code(6));
    ASSERT_EQ("11111", get_gray_code(21));
    ASSERT_EQ("101101", get_gray_code(54));
}

TEST(test_p10, gray_decode) {
    for (auto i = 0; i < 102; ++i)
        ASSERT_EQ(i, get_number(gray_decode(get_gray_code(i))));
}

TEST(test_p10, solution_gray_encode) {
    ASSERT_EQ(0, solution::gray_encode(0));
    ASSERT_EQ(1, solution::gray_encode(1));
    ASSERT_EQ(3, solution::gray_encode(2));
    ASSERT_EQ(2, solution::gray_encode(3));
    ASSERT_EQ(5, solution::gray_encode(6));
    ASSERT_EQ(31, solution::gray_encode(21));
    ASSERT_EQ(45, solution::gray_encode(54));
}

TEST(test_p10, solution_gray_decode) {
    for (auto i = 0; i < 102; ++i)
        ASSERT_EQ(i, solution::gray_decode(solution::gray_encode(i)));
}