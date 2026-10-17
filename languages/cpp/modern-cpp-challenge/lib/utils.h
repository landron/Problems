#pragma once

#include <string>
#include <vector>

namespace utils {

template <typename T>
std::string to_string(const std::vector<T>&);
std::string to_string_impl(const std::vector<size_t>&);
std::string to_string(const std::vector<std::pair<unsigned, unsigned>>&);

template <>
inline std::string to_string(const std::vector<size_t>& vec) {
    return to_string_impl(vec);
}

template <typename T>
inline std::string to_string(const std::vector<T>& vec) {
    std::vector<size_t> vec2(vec.begin(), vec.end());
    return to_string_impl(vec2);
}

}; // namespace utils
