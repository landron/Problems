/*
./topics --gtest_filter=WavinessTest.Minimal
./topics --gtest_filter=WavinessTest.*
*/
#include <gtest/gtest.h>

#include "001_waviness_brute.h"
#include "001_waviness_digit_dp.h"

template <typename T>
void runMinimalTest() {
    EXPECT_EQ(3, T().totalWaviness(120, 130));
    EXPECT_EQ(3, T().totalWaviness(198, 202));
    EXPECT_EQ(2, T().totalWaviness(4848, 4848));
    EXPECT_EQ(0, T().totalWaviness(0, 100));
    EXPECT_EQ(1, T().totalWaviness(0, 101));
}

TEST(WavinessTest, Minimal) {
    runMinimalTest<waviness::SolutionBrute>();
    runMinimalTest<waviness::SolutionDigitDP>();
}

template <typename T>
void runEdgeCases() {
    EXPECT_EQ(1, T().totalWaviness(198, 198));
    EXPECT_EQ(0, T().totalWaviness(100, 100));
    EXPECT_EQ(0, T().totalWaviness(1331, 1331)); // no peak, but flat
    EXPECT_EQ(1, T().totalWaviness(131, 131));
    EXPECT_EQ(2, T().totalWaviness(1212, 1212));
    EXPECT_EQ(0, T().totalWaviness(1111, 1111));
}

TEST(WavinessTest, EdgeCases) {
    runEdgeCases<waviness::SolutionBrute>();
    runEdgeCases<waviness::SolutionDigitDP>();
}

TEST(WavinessTest, TimeoutTest) {
    waviness::SolutionDigitDP sol;
    EXPECT_EQ(11'661'365'485, sol.totalWaviness(2'549'294'942, 5'067'104'447));
}
