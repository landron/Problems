#[[
	* go to build folder
	* cmake -G Ninja <path to this CMakeLists.txt folder>
	* ninja

	with build folder outside this repository, you can do:
		cmake -G Ninja ../../Problems/hackerrank/algo
]]
cmake_minimum_required(VERSION 3.21...4.2)

# https://vcpkg.readthedocs.io/en/latest/users/integration/
if(DEFINED ENV{VCPKG_ROOT} AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE FILEPATH "")
endif()

project(hackerrank_algo)
add_executable(${PROJECT_NAME} bsearch/find_first_occurence.cpp)

set_target_properties(${PROJECT_NAME} PROPERTIES
    CXX_STANDARD 23
    CXX_STANDARD_REQUIRED YES
    CXX_EXTENSIONS NO
)

# Enable common warnings - vital for troubleshooting performance/bugs
if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE /W4 /WX)
else()
    target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

find_package(GTest MODULE REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE GTest::GTest GTest::Main)
