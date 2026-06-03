#[[
    cmake -G Ninja ../../mine/problems
]]
cmake_minimum_required(VERSION 3.21...4.2)

# https://vcpkg.readthedocs.io/en/latest/users/integration/
if(DEFINED ENV{VCPKG_ROOT} AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE FILEPATH "")
endif()

set(CMAKE_CXX_STANDARD 26)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(formatter)

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
