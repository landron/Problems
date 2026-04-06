"""Find shortest paths in graph where each node incurs a processing cost.

https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/shortest-path-with-processing-delays/

Complexity: O(N + M*M) Time (Dijkstra variant) | O(N + M) Space
Tags: #dijkstra #shortest-path #graph
Compliance: ruff & pylint clean.
"""

import bisect
import sys
import unittest


def compute_cost_mine(costs, edges, source):
    """Find shortest paths with processing delays (custom algorithm).

    Complexity: O(n + m + m*n) = O(m*n) Time | O(N + M) Space

    WARNING: 12/15 test cases passed.
    WARNING: Keep algorithm logic intact - only pylint compliance.
    """

    def build_adjacency_list(n, edges):
        """Build adjacency list, keeping minimum weight for duplicate edges."""
        neighbors = {i: {} for i in range(n)}
        for i, j, w in edges:
            if i == j:
                continue
            if j not in neighbors[i] or neighbors[i][j] > w:
                neighbors[i][j] = w
        return neighbors

    n = len(costs)
    neighbors = build_adjacency_list(n, edges)
    visited = {}

    def check_visited(edge, visited):
        x, y = edge
        assert 0 <= x < n and 0 <= y < n and x != y
        ret = visited.get((x, y), False)
        visited[(x, y)] = True
        return ret

    min_costs = [-1] * n
    min_costs[source] = 0  # cost[0] doesn't matter
    stack = [source]
    while stack:
        current = stack.pop()
        if current == source:
            visited = {}
        for neighbor, weight in neighbors[current].items():
            if check_visited((current, neighbor), visited):
                continue
            min_cost = min_costs[current] + costs[current] + weight
            if current == source:
                min_cost -= costs[current]
            if min_costs[neighbor] != -1 and min_costs[neighbor] < min_cost:
                continue
            min_costs[neighbor] = min_cost
            stack.append(neighbor)
    return min_costs


def compute_cost_dijkstra(costs, edges, source):
    """Dijkstra's algorithm with processing delays.

    Complexity: O(n + m*m) Time | O(N + M) Space
        Time: O(n + m*m) - bisect.insort is O(m) per insertion, O(m) insertions.
        Space: O(n + m)

    Note: 15/15 test cases passed.
    TODO: Optimize to O(m*log(m)) using priority queue.
    """
    n = len(costs)
    neighbors = {i: {} for i in range(n)}
    for i, j, w in edges:
        if i == j:
            continue
        # keep minimum weight if multiple edges to same destination
        if j not in neighbors[i] or neighbors[i][j] > w:
            neighbors[i][j] = w

    min_costs = [-1] * n
    min_costs[source] = 0
    visited = set([source])
    unvisited = []
    for i, w in neighbors[source].items():
        # costs[source] is ignored
        min_costs[i] = w
        bisect.insort(unvisited, (w, i))

    while unvisited:
        current_cost, current = unvisited.pop(0)
        # second check: ignore older (higher) costs for the same node
        if current in visited or current_cost != min_costs[current]:
            continue

        visited.add(current)
        for i, w in neighbors[current].items():
            if i in visited:
                continue
            min_cost = current_cost + costs[current] + w
            if min_costs[i] != -1 and min_costs[i] <= min_cost:
                continue
            min_costs[i] = min_cost
            # older costs will be ignored because of the check at the beginning of the loop
            bisect.insort(unvisited, (min_cost, i))

    return min_costs


def main():
    """Run basic tests for shortest path algorithms."""
    result = compute_cost_mine([1, 2, 3], [[0, 1, 4], [1, 2, 5], [0, 2, 10]], 0)
    assert result == [0, 4, 10]
    result = compute_cost_mine(
        [0, 5, 2, 3, 4],
        [[0, 1, 2], [0, 2, 8], [1, 3, 7], [2, 3, 1], [3, 4, 3], [1, 4, 15]],
        0,
    )
    assert result == [0, 2, 8, 11, 17]
    print("All tests passed!")


class TestComputeCost(unittest.TestCase):
    """Unit tests for shortest path with processing delays"""

    def test_basic_path_with_processing(self):
        """Test basic graph with processing delays"""
        test_cases = [
            {
                "costs": [1, 2, 3],
                "edges": [[0, 1, 4], [1, 2, 5], [0, 2, 10]],
                "expected": [0, 4, 10],
            },
            {
                "costs": [0, 5, 2, 3, 4],
                "edges": [
                    [0, 1, 2],
                    [0, 2, 8],
                    [1, 3, 7],
                    [2, 3, 1],
                    [3, 4, 3],
                    [1, 4, 15],
                ],
                "expected": [0, 2, 8, 11, 17],
            },
        ]
        for case in test_cases:
            result = compute_cost_mine(case["costs"], case["edges"], 0)
            self.assertEqual(result, case["expected"])
            result = compute_cost_dijkstra(case["costs"], case["edges"], 0)
            self.assertEqual(result, case["expected"])

    def test_complex_path(self):
        """Test more complex graph"""
        result = compute_cost_dijkstra(
            [0, 5, 2, 3, 4],
            [[0, 1, 2], [0, 2, 8], [1, 3, 7], [2, 3, 1], [3, 4, 3], [1, 4, 15]],
            0,
        )
        self.assertEqual(result, [0, 2, 8, 11, 17])

    def test_duplicate_edges_two(self):
        """Test that minimum edge weight is selected when two edges exist"""
        result = compute_cost_dijkstra([0, 1, 1], [[0, 1, 5], [0, 1, 3]], 0)
        self.assertEqual(result, [0, 3, -1])
        result = compute_cost_mine([0, 1, 1], [[0, 1, 5], [0, 1, 3]], 0)
        self.assertEqual(result, [0, 3, -1])

    def test_duplicate_edges_three(self):
        """Test that minimum edge weight is selected when multiple edges exist"""
        result = compute_cost_dijkstra([0, 2, 2], [[0, 1, 10], [0, 1, 4], [0, 1, 7]], 0)
        self.assertEqual(result, [0, 4, -1])
        result = compute_cost_mine([0, 2, 2], [[0, 1, 10], [0, 1, 4], [0, 1, 7]], 0)
        self.assertEqual(result, [0, 4, -1])

    def test_unreachable_node(self):
        """Test that unreachable nodes return -1"""
        result = compute_cost_dijkstra([0, 1], [[0, 0, 5]], 0)
        self.assertEqual(result, [0, -1])
        result = compute_cost_mine([0, 1], [[0, 0, 5]], 0)
        self.assertEqual(result, [0, -1])

    def test_single_node(self):
        """Test with single node"""
        result = compute_cost_dijkstra([5], [], 0)
        self.assertEqual(result, [0])
        result = compute_cost_mine([5], [], 0)
        self.assertEqual(result, [0])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "main":
        main()
    else:
        unittest.main()
