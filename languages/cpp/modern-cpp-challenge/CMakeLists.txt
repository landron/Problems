#[[
    cmake -G Ninja ../../mine/problems/languages/cpp/modern-cpp-challenge
        -DCMAKE_BUILD_TYPE=Debug : debug (debug symbols, step debugging)

    Commands
        VsDevCmd.bat -arch=amd64
        cd F:\_Devel\build\modern-cpp-challenge-cmd
            go to the build directory
        cmake -G Ninja -DCMAKE_BUILD_TYPE=Debug <path to CMakeLists.txt folder>
        (or RelWithDebInfo)

        vcpkg install gtest --triplet x64-windows
        (or 64-linux)

    "The package gtest is compatible with built-in CMake targets:
        enable_testing()
        find_package(GTest MODULE REQUIRED)
        target_link_libraries(main PRIVATE GTest::GTest GTest::Main)
        add_test(AllTestsInMain main)
    "

    \todo :
        * multiple configurations with VS Community 2017, 15.9.x
            (meaning? using clang ?)
        * clang-format

    Knowledge base
        * fast command line build with Ninja:
            see https://github.com/landron/workshop/tree/master/c%2B%2B/01-cmake,
                    4.Windows, Visual Studio 15 2017, Ninja
                    ! VsDevCmd.bat -arch=amd64
            modern-cpp-challenge --gtest_list_tests
            modern-cpp-challenge --gtest_filter=test_p03*

            modern-cpp-challenge --gtest_filter=test_main*

        * CMake GUI: "Delete cache" after defining VCPKG_ROOT
            (set DOS command)
        * update vcpkg: git pull, bootstrap-vcpkg.bat
        * update packages: see vcpkg parameters

        * VC Code integration on Linux: see https://code.visualstudio.com/docs/cpp/cmake-linux
    ]]
cmake_minimum_required(VERSION 3.21...4.2)

#
#   vcpkg
#
# https://vcpkg.readthedocs.io/en/latest/users/integration/
if(DEFINED ENV{VCPKG_ROOT} AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    set(VCPKG_ROOT "$ENV{VCPKG_ROOT}")
    message(STATUS "VCPKG_ROOT=${VCPKG_ROOT}")
    set(CMAKE_TOOLCHAIN_FILE "${VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE FILEPATH "")
endif()

#
#   build type: -DCMAKE_BUILD_TYPE=Release/Debug/RelWithDebInfo/MinSizeRel
#       see CMakeCache.txt
#
# message(CMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE})
#message(CMAKE_CONFIGURATION_TYPES=${CMAKE_CONFIGURATION_TYPES})

#
#   The project
#

set(CMAKE_CXX_STANDARD 26)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(modern-cpp-challenge)

find_package(GTest MODULE REQUIRED)

set(sources main.cpp problems.h lib/my_math.h lib/math.cpp lib/utils.h lib/utils.cpp)
file(GLOB_RECURSE PROBLEM_FILES "${PROJECT_SOURCE_DIR}/p*.cpp")
set(sources ${sources} ${PROBLEM_FILES})
add_executable(${PROJECT_NAME} ${sources})
# it also adds include path
target_link_libraries(${PROJECT_NAME} PRIVATE GTest::GTest GTest::Main)

# TODO: cl : Command line warning D9025 : overriding '/W3' with '/W4'
#[[
target_compile_options(${PROJECT_NAME} PRIVATE
  $<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
  $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -pedantic -Werror>
)
]]
