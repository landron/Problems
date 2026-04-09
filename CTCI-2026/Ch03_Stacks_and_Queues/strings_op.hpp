#pragma once

#include <algorithm>
#include <cctype>
#include <ranges>
#include <string_view>
#include <string>

#include <gtest/gtest.h>

namespace {

[[nodiscard]] auto trim_and_lower(std::string_view str) -> std::string {
    auto is_space = [](unsigned char c) { return std::isspace(c); };

    return str 
         | std::views::drop_while(is_space)               // Front trim
         | std::views::reverse                            // Flip
         | std::views::drop_while(is_space)               // Back trim (while flipped)
         | std::views::reverse                            // Flip back
         | std::views::transform([](unsigned char c) {    // Lowercase
               return static_cast<char>(std::tolower(c)); 
           })
         | std::ranges::to<std::string>();                // Collect
}


[[nodiscard]] auto trim_and_lower_old(std::string_view str) -> std::string {
    static constexpr std::string_view whitespace = " \t\n\r\f\v";
    
    const auto start = str.find_first_not_of(whitespace);
    if (start == std::string_view::npos) return "";
    
    const auto end = str.find_last_not_of(whitespace);
    str = str.substr(start, end - start + 1);
    
    std::string result(str);
    std::ranges::transform(result, result.begin(), 
                          [](unsigned char c) { return std::tolower(c); });
    return result;
}

/*
Each time you add a pipe (|), the return type becomes a deeply nested template 
wrapped in the previous one.
*/
[[nodiscard]] auto trim_and_lower_modern(std::string_view str) -> std::string {
    auto is_space = [](unsigned char c) { return std::isspace(c); };

    // Drop leading whitespace
    auto trimmed = str | std::views::drop_while(is_space);

    // Drop trailing whitespace by reversing, dropping, then reversing back
    auto back_trimmed = trimmed 
                      | std::views::reverse 
                      | std::views::drop_while(is_space) 
                      | std::views::reverse;

    // Transform to lower case and collect into a string
    return back_trimmed 
         | std::views::transform([](unsigned char c) { 
               return static_cast<char>(std::tolower(c)); 
           })
         | std::ranges::to<std::string>(); 
}

// Test all three variants
void expect_all_variants(std::string_view input, const std::string& expected) {
    EXPECT_EQ(trim_and_lower_old(input), expected) << "trim_and_lower_old failed";
    EXPECT_EQ(trim_and_lower_modern(input), expected) << "trim_and_lower_modern failed";
    EXPECT_EQ(trim_and_lower(input), expected) << "trim_and_lower failed";
}

}  // anonymous namespace

TEST(TrimAndLower, EmptyString) {
    expect_all_variants("", "");
}

TEST(TrimAndLower, OnlyWhitespace) {
    expect_all_variants("   ", "");
    expect_all_variants("\t\n\r", "");
    expect_all_variants("  \t  \n  \r  ", "");
}

TEST(TrimAndLower, NoWhitespace) {
    expect_all_variants("hello", "hello");
    expect_all_variants("HELLO", "hello");
    expect_all_variants("HeLLo", "hello");
}

TEST(TrimAndLower, LeadingWhitespace) {
    expect_all_variants("  hello", "hello");
    expect_all_variants("\t\thello", "hello");
    expect_all_variants("\n\nhello", "hello");
}

TEST(TrimAndLower, TrailingWhitespace) {
    expect_all_variants("hello  ", "hello");
    expect_all_variants("hello\t\t", "hello");
    expect_all_variants("hello\n\n", "hello");
}

TEST(TrimAndLower, BothWhitespace) {
    expect_all_variants("  hello  ", "hello");
    expect_all_variants("\t\thello\t\t", "hello");
    expect_all_variants("\n\nhello\n\n", "hello");
    expect_all_variants("  \t HELLO \n  ", "hello");
}

TEST(TrimAndLower, InternalWhitespace) {
    expect_all_variants("hello world", "hello world");
    expect_all_variants("  hello   world  ", "hello   world");
    expect_all_variants("HELLO WORLD", "hello world");
    expect_all_variants("  HELLO   WORLD  ", "hello   world");
}

TEST(TrimAndLower, MixedCaseAndWhitespace) {
    expect_all_variants("  HeLLo WoRLd  ", "hello world");
    expect_all_variants("\tTeSt\n", "test");
    expect_all_variants("  MiXeD CaSe  ", "mixed case");
}

TEST(TrimAndLower, SpecialCharacters) {
    expect_all_variants("  123!@#  ", "123!@#");
    expect_all_variants("  hello-world  ", "hello-world");
    expect_all_variants("  HELLO_WORLD  ", "hello_world");
}

TEST(TrimAndLower, SingleCharacter) {
    expect_all_variants("A", "a");
    expect_all_variants("  A  ", "a");
    expect_all_variants("a", "a");
    expect_all_variants("  a  ", "a");
}
