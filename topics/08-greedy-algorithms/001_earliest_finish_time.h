/*
    https://leetcode.com/problems/earliest-finish-time-for-land-and-water-rides-ii/

#ds_vector
#algo_greedy
#algo_linear_scan           // linear time without sorting
#tech_cache_locality
#tech_eliminate_sorting
#pattern_earliest_finish
#perf_zero_allocation
*/
#pragma once

#include <algorithm>
#include <cassert>
#include <vector>

/*
Performance & Architectural Differences
Metric	            Original Code	Modernized Code	    Why?
Time Complexity	    O(NlogN)	    O(N)	            Eliminated sorting
                                                        entirely.
Space Complexity	O(N)	        O(1)	            Zero vector
        allocations or temporary pair zipping.
Memory Access	    High Overhead   Cache-Friendly	    Removed raw .at()
        bounds checking inside lambda lookups.Loops scan flat
        contiguous memory fields linearly.

Runtime
0ms
Beats   100.00%
Memory
238.03MB
Beats   66.06%
*/
class SolutionGemini {
  public:
    int earliestFinishTime(const std::vector<int>& landStartTime,
                           const std::vector<int>& landDuration,
                           const std::vector<int>& waterStartTime,
                           const std::vector<int>& waterDuration) {
        assert(!landStartTime.empty() && !waterStartTime.empty());

        // 1. Find the global earliest standalone finish time for land
        int min_land_finish = landStartTime[0] + landDuration[0];
        for (size_t i = 1; i < landStartTime.size(); ++i) {
            min_land_finish =
                std::min(min_land_finish, landStartTime[i] + landDuration[i]);
        }

        // 2. Find the global earliest standalone finish time for water
        int min_water_finish = waterStartTime[0] + waterDuration[0];
        for (size_t i = 1; i < waterStartTime.size(); ++i) {
            min_water_finish = std::min(min_water_finish,
                                        waterStartTime[i] + waterDuration[i]);
        }

        // 3. Chain the sequences sequentially using the raw inputs
        const auto land_then_water = earliestFinishTimeAfter(
            waterStartTime, waterDuration, min_land_finish);
        const auto water_then_land = earliestFinishTimeAfter(
            landStartTime, landDuration, min_water_finish);

        return std::min(land_then_water, water_then_land);
    }

  private:
    // Pure O(N) allocation-free sequential sweep
    static int earliestFinishTimeAfter(const std::vector<int>& start,
                                       const std::vector<int>& duration,
                                       int after_time) {

        auto absolute_best_finish =
            std::max(after_time, start[0]) + duration[0];
        for (size_t i = 1; i < start.size(); ++i) {
            auto current_finish = std::max(after_time, start[i]) + duration[i];
            if (current_finish < absolute_best_finish) {
                absolute_best_finish = current_finish;
            }
        }

        return absolute_best_finish;
    }
};

class SolutionMine {
  public:
    int earliestFinishTime(std::vector<int>& landStartTime,
                           std::vector<int>& landDuration,
                           std::vector<int>& waterStartTime,
                           std::vector<int>& waterDuration) {
        assert(!landStartTime.empty());
        assert(!waterStartTime.empty());

        auto earlier = [&](size_t idx, size_t best, bool is_land) {
            auto start = &landStartTime;
            auto duration = &landDuration;
            if (!is_land) {
                start = &waterStartTime;
                duration = &waterDuration;
            }
            auto hour_best = start->at(best) + duration->at(best);
            // not sorted
            // if (hour_best <= start->at(idx)) return 0;
            auto hour_new = start->at(idx) + duration->at(idx);
            if (hour_best > hour_new) return 1;
            if (hour_best == hour_new && duration->at(idx) < duration->at(best))
                return 1;
            return 2;
        };

        auto firstLandEnd = 0, firstWaterEnd = 0;
        for (size_t i = 0; i < landStartTime.size(); ++i) {
            auto ret = earlier(i, firstLandEnd, true);
            if (ret == 0) break;
            if (ret == 1) firstLandEnd = i;
        }
        for (size_t i = 0; i < waterStartTime.size(); ++i) {
            auto ret = earlier(i, firstWaterEnd, false);
            if (ret == 0) break;
            if (ret == 1) firstWaterEnd = i;
        }

        auto finish_time = [&](size_t idx, bool is_land) {
            if (is_land) return landStartTime[idx] + landDuration[idx];
            return waterStartTime[idx] + waterDuration[idx];
        };

        auto firstLand = earliestFinishTimeAfter(
            waterStartTime, waterDuration, finish_time(firstLandEnd, true));
        auto firstWater = earliestFinishTimeAfter(
            landStartTime, landDuration, finish_time(firstWaterEnd, false));
        // std::cout << firstLand << ", " << firstWater << std::endl;
        return (firstLand < firstWater) ? firstLand : firstWater;
    }

  private:
    int earliestFinishTimeAfter(const std::vector<int>& start,
                                const std::vector<int>& duration, int after) {
        std::vector<std::pair<int, int>> intervals;
        intervals.reserve(start.size());
        for (size_t i = 0; i < start.size(); ++i) {
            intervals.push_back({start[i], duration[i]});
        }
        // O(N*logN)
        std::sort(intervals.begin(), intervals.end());

        auto best = ((after < intervals.front().first) ? intervals.front().first
                                                       : after) +
                    intervals.front().second;
        // O(N)
        for (size_t i = 0; i < intervals.size(); ++i) {
            if (best <= intervals[i].first) break;
            auto next =
                ((after < intervals[i].first) ? intervals[i].first : after) +
                intervals[i].second;
            if (next < best) best = next;
        }
        return best;
    }
};
