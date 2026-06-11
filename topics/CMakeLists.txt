#[[
	cmake -G Ninja ../../mine/problems/topics

    ./topics --gtest_filter=EarliestFinishTime.*
]]
#[[
	Categories:
        01. Arrays and Basic Problem Solving
        02. Strings and Pattern Matching
        03. Linked Lists
        04. Stacks and Queues
        05. Binary Search
        06. Two Pointers and Sliding Window
        07. Hash Tables and Hash Maps
        08. Greedy Algorithms
        09. Backtracking and Recursion
        10. Dynamic Programming Fundamentals
        11. Trees and Binary Search Trees
        12. Graphs
        13. Sorting and Selection
        14. Heaps and Priority Queues
        15. Interval and Scheduling Problems
        16. Mathematical / Number Theory
        17. Bit Manipulation
]]
cmake_minimum_required(VERSION 3.21...4.2)

# https://vcpkg.readthedocs.io/en/latest/users/integration/
if(DEFINED ENV{VCPKG_ROOT} AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE FILEPATH "")
endif()

set(CMAKE_CXX_STANDARD 26)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(topics)

add_executable(
    ${PROJECT_NAME}
    08-greedy-algorithms/001_earliest_finish_time_test.cpp
    10-dynamic-programming/001_waviness_test.cpp 10-dynamic-programming/002_max_sum_non_overlapping_subarrays_test.cpp
)

# Enable common warnings - vital for troubleshooting performance/bugs
if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE /W4 /WX)
else()
    target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

find_package(GTest MODULE REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE GTest::GTest GTest::Main)
