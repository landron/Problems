/*
        Purpose
                measure duration, but not useful with Google Test which also
   does it (in ms)

        Reference
                https://stackoverflow.com/questions/2808398/easily-measure-elapsed-time
*/
#pragma once

#include <chrono>
#include <iomanip>
#include <iostream>

namespace utils {

class Duration {
  public:
    explicit Duration(const char* measure_object)
        : m_measure_object(measure_object) {}

    ~Duration() {
        const auto end = std::chrono::steady_clock::now();
        const auto duration_s =
            (std::chrono::duration_cast<std::chrono::microseconds>(end -
                                                                   m_begin)
                 .count()) /
            1000000.0;
        if (duration_s > 0.1) {
            const auto precision = std::cout.precision();
            // necessary to avoid scientific
            std::cout << std::fixed;
            std::cout << std::setprecision(2);
            std::cout << "Time difference for \"" << m_measure_object
                      << "\" is ";
            std::cout << duration_s << " seconds." << std::endl;
            std::cout << std::setprecision(precision);
        }
    }

  private:
    const std::string m_measure_object;
    const std::chrono::steady_clock::time_point m_begin =
        std::chrono::steady_clock::now();
};

} // namespace utils
