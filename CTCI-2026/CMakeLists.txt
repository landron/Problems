#[[
	* go to build folder
	* cmake -G Ninja <path to this CMakeLists.txt folder>
	* ninja

	with build folder outside this repository, you can do:
		cmake -G Ninja ../Problems/CTCI-2026

	Cracking the Coding Interview
]]

cmake_minimum_required(VERSION 3.21...4.2)


set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(ctci-2026)

add_executable(${PROJECT_NAME} Ch02_Linked_Lists/q2_2_kth_to_last.cpp)

# Enable common warnings - vital for troubleshooting performance/bugs
if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE /W4 /WX)
else()
    target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

find_package(GTest MODULE REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE GTest::GTest GTest::Main)
