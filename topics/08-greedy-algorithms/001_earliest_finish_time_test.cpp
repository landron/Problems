/*
./topics --gtest_filter=EarliestFinishTime.Minimal
./topics --gtest_filter=EarliestFinishTime.*
*/
#include <gtest/gtest.h>

#include "001_earliest_finish_time.h"

template <typename T>
void runMinimalTest() {
    std::vector<int> landS = {1};
    std::vector<int> landD = {3};
    std::vector<int> waterS = {10};
    std::vector<int> waterD = {2};

    T sol;
    EXPECT_EQ(sol.earliestFinishTime(landS, landD, waterS, waterD), 12);
}

TEST(EarliestFinishTime, Minimal) {
    runMinimalTest<SolutionMine>();
    runMinimalTest<SolutionGemini>();
}

template <typename T>
void runWaterThenLandIsBetterTest() {
    std::vector<int> landS = {10, 100};
    std::vector<int> landD = {10, 10};

    std::vector<int> waterS = {1};
    std::vector<int> waterD = {5};

    T sol;

    // water ends at 6, then land at 10 → finish 20
    EXPECT_EQ(sol.earliestFinishTime(landS, landD, waterS, waterD), 20);
}

TEST(EarliestFinishTime, WaterThenLandIsBetter) {
    runWaterThenLandIsBetterTest<SolutionMine>();
    runWaterThenLandIsBetterTest<SolutionGemini>();
}

template <typename T>
void runLandThenWaterBetterTest() {
    std::vector<int> landS = {1};
    std::vector<int> landD = {2};

    std::vector<int> waterS = {10, 100};
    std::vector<int> waterD = {2, 2};

    T sol;
    EXPECT_EQ(sol.earliestFinishTime(landS, landD, waterS, waterD), 12);
}

TEST(EarliestFinishTime, LandThenWaterBetter) {
    runLandThenWaterBetterTest<SolutionMine>();
    runLandThenWaterBetterTest<SolutionGemini>();
}

template <typename T>
void runMustWaitTest() {
    std::vector<int> landS = {1};
    std::vector<int> landD = {5};

    std::vector<int> waterS = {20};
    std::vector<int> waterD = {1};

    T sol;
    EXPECT_EQ(sol.earliestFinishTime(landS, landD, waterS, waterD), 21);
}

TEST(EarliestFinishTime, MustWait) {
    runMustWaitTest<SolutionMine>();
    runMustWaitTest<SolutionGemini>();
}

template <typename T>
void runBestPairSelectionTest() {
    std::vector<int> landS = {1, 5, 10};
    std::vector<int> landD = {5, 2, 2};

    std::vector<int> waterS = {3, 8};
    std::vector<int> waterD = {5, 1};

    T sol;
    EXPECT_EQ(sol.earliestFinishTime(landS, landD, waterS, waterD), 9);
}

TEST(EarliestFinishTime, BestPairSelection) {
    runBestPairSelectionTest<SolutionMine>();
    runBestPairSelectionTest<SolutionGemini>();
}

template <typename T>
void runLargeGapTest() {
    std::vector<int> landS = {1, 50};
    std::vector<int> landD = {1, 1};

    std::vector<int> waterS = {10, 20};
    std::vector<int> waterD = {1, 1};

    T sol;
    EXPECT_EQ(sol.earliestFinishTime(landS, landD, waterS, waterD), 11);
}

TEST(EarliestFinishTime, LargeGap) {
    runLargeGapTest<SolutionMine>();
    runLargeGapTest<SolutionGemini>();
}

template <typename T>
void runTieCaseTest() {
    std::vector<int> landS = {1, 1};
    std::vector<int> landD = {3, 2};

    std::vector<int> waterS = {4, 4};
    std::vector<int> waterD = {1, 1};

    T sol;
    EXPECT_EQ(sol.earliestFinishTime(landS, landD, waterS, waterD), 5);
}

TEST(EarliestFinishTime, TieCases) {
    runTieCaseTest<SolutionMine>();
    runTieCaseTest<SolutionGemini>();
}

template <typename T>
void runConsistencyTest() {
    std::vector<int> landS = {1, 2, 3};
    std::vector<int> landD = {5, 5, 5};

    std::vector<int> waterS = {10, 11, 12};
    std::vector<int> waterD = {1, 1, 1};

    T sol;
    EXPECT_EQ(sol.earliestFinishTime(landS, landD, waterS, waterD), 11);
}

TEST(EarliestFinishTime, Consistency) {
    runConsistencyTest<SolutionMine>();
    runConsistencyTest<SolutionGemini>();
}

// some original problem tests

template <typename T>
void runSample1Test() {
    std::vector<int> landS = {5};
    std::vector<int> landD = {3};

    std::vector<int> waterS = {1};
    std::vector<int> waterD = {10};

    T sol;
    EXPECT_EQ(sol.earliestFinishTime(landS, landD, waterS, waterD), 14);
}

TEST(EarliestFinishTime, Sample1) {
    runSample1Test<SolutionMine>();
    runSample1Test<SolutionGemini>();
}

template <typename T>
void runSample2Test() {
    std::vector<int> landS = {2, 8};
    std::vector<int> landD = {4, 1};

    std::vector<int> waterS = {6};
    std::vector<int> waterD = {3};

    T sol;
    EXPECT_EQ(sol.earliestFinishTime(landS, landD, waterS, waterD), 9);
}

TEST(EarliestFinishTime, Sample2) {
    runSample2Test<SolutionMine>();
    runSample2Test<SolutionGemini>();
}

template <typename T>
void runSample3Test() {
    std::vector<int> landS = {82, 14};
    std::vector<int> landD = {42, 30};

    std::vector<int> waterS = {6, 54};
    std::vector<int> waterD = {91, 71};

    T sol;
    EXPECT_EQ(sol.earliestFinishTime(landS, landD, waterS, waterD), 125);
}

TEST(EarliestFinishTime, Sample3) {
    runSample3Test<SolutionMine>();
    runSample3Test<SolutionGemini>();
}
