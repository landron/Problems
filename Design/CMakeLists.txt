#[[
    cmake -G Ninja ../../Problems/CTCI-2026
        with build folder outside this repository, you can do:
        cmake -G Ninja ../../mine/problems/Design
]]
cmake_minimum_required(VERSION 3.21...4.2)

# https://vcpkg.readthedocs.io/en/latest/users/integration/
if(DEFINED ENV{VCPKG_ROOT} AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE FILEPATH "")
endif()

set(CMAKE_CXX_STANDARD 26)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(design)

# Source files for the executable
file(GLOB_RECURSE SOURCES *.cpp)

add_executable(
    ${PROJECT_NAME}
    ${SOURCES}
)

# Enable common warnings - vital for troubleshooting performance/bugs
if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE /W4 /WX)
else()
    target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

find_package(GTest MODULE REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE GTest::GTest GTest::Main)

find_program(CLANG_FORMAT "clang-format")

if(CLANG_FORMAT)
    # Get all project source files
    file(GLOB_RECURSE ALL_SOURCE_FILES *.cpp *.h *.hpp *.cc)

    add_custom_target(format
        # -style=file:${CMAKE_SOURCE_DIR}/.clang-format
        COMMAND ${CLANG_FORMAT} -i ${ALL_SOURCE_FILES}
        COMMENT "Formatting code with clang-format"
    )
else()
    message(WARNING "clang-format not found. 'format' target will not be available.")
endif()
