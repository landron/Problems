#pragma once

#include <vector>

using Grid = std::vector<std::vector<unsigned>>;

namespace diagonal_sudoku_dfs {

Grid solve(const Grid& board);

}
