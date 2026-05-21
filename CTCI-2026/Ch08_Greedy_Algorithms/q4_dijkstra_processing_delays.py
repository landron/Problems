"""Find shortest paths in graph where each node incurs a processing cost.

https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/shortest-path-with-processing-delays/

While the problem takes place on a graph, the actual algorithmic tool used to
solve it is Dijkstra's Algorithm (or a slight modification of it to account
for node weights instead of just edge weights).
 * Dijkstra's algorithm is fundamentally classified as a Greedy Algorithm.
 * At every single step, it makes a locally optimal choice: it grabs the next
 unvisited node with the absolute lowest accumulated cost (processing delay +
 travel time) from the priority queue. It assumes that this immediate local
 best choice will yield the globally optimal shortest path

Complexity: O(N + M*M) Time (Dijkstra variant) | O(N + M) Space
Tags: #dijkstra #shortest-path #graph
Compliance: black, pylint, ruff
    ruff check Ch04_Trees_and_Graphs/q4_dijkstra_processing_delays.py
"""

import bisect
import heapq
import sys
import unittest


def _build_adjacency_list(n, edges):
    """Build adjacency list, keeping minimum weight for duplicate edges.

    OPT: List of Lists of Tuples (instead of Dict of Dicts) would be more space-efficient,
        but less convenient for duplicate edge handling.
    """
    neighbors = {i: {} for i in range(n)}
    for i, j, w in edges:
        if i == j:
            continue
        if j not in neighbors[i] or neighbors[i][j] > w:
            neighbors[i][j] = w
    return neighbors


def compute_cost_dijkstra_heapq(costs, edges, source):
    """Dijkstra's algorithm with processing delays using min-heap.

    Complexity: O((n + m)*log(m)) Time | O(N + M) Space
        Time: O((n + m)*log(m)) - heappush/heappop are O(log m),
              called O(n + m) times for at most O(m) relaxations.
        Space: O(n + m)
    Note: complexity drops from O(m*n) to O((n + m)*log(m)) by using a priority
        queue (min-heap) instead of a sorted list.

    Note: Tuples (cost, node) work with heapq because Python compares
        lexicographically: first by cost, then by node index as tiebreaker.
    """
    n = len(costs)
    neighbors = _build_adjacency_list(n, edges)

    min_costs = [-1] * n
    min_costs[source] = 0
    visited = set([source])
    heap = []
    for i, w in neighbors[source].items():
        # costs[source] is ignored
        min_costs[i] = w
        # heappush with (cost, node) tuple: heap orders by cost; node breaks ties
        heapq.heappush(heap, (w, i))

    while heap:
        current_cost, current = heapq.heappop(heap)
        # ignore older (higher) costs for the same node
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
            heapq.heappush(heap, (min_cost, i))

    return min_costs


def compute_cost_dijkstra(costs, edges, source):
    """Dijkstra's algorithm with processing delays.

    Complexity: O(n + m*m) Time | O(N + M) Space
        Time: O(n + m*m) - bisect.insort is O(m) per insertion (O(log m) search +
              O(m) shift), with O(m) insertions max.
        Space: O(n + m)

    Note: Optimized to O(m*log(m)) using priority queue (heapq variant exists).
    """
    n = len(costs)
    neighbors = _build_adjacency_list(n, edges)

    min_costs = [-1] * n
    min_costs[source] = 0
    visited = set([source])
    unvisited = []
    for i, w in neighbors[source].items():
        # costs[source] is ignored
        min_costs[i] = w
        # bisect.insort: O(m) per call (binary search O(log m) + shift O(m))
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
            # Reinsert: O(m) cost. Duplicates filtered by re-check at loop start.
            bisect.insort(unvisited, (min_cost, i))

    return min_costs


def compute_cost_mine(costs, edges, source):
    """Find shortest paths with processing delays (custom algorithm).

    Complexity: O(n + m + m*n) = O(m*n) Time | O(N + M) Space

    WARNING: 12/15 test cases passed. @hackerrank
        check_visited marks edges permanently per source-traversal,
        so cheaper paths found later can't re-explore outgoing edges.
        See test_mine_fails_longer_relay_path, test_mine_fails_indirect_cheaper_path.
    WARNING: Keep algorithm logic intact - only pylint compliance.
    """

    n = len(costs)
    neighbors = _build_adjacency_list(n, edges)
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
            result_mine = compute_cost_mine(case["costs"], case["edges"], 0)
            self.assertEqual(result_mine, case["expected"])
            result_bisect = compute_cost_dijkstra(case["costs"], case["edges"], 0)
            self.assertEqual(result_bisect, case["expected"])
            result_heapq = compute_cost_dijkstra_heapq(case["costs"], case["edges"], 0)
            self.assertEqual(result_heapq, case["expected"])

    def test_complex_path(self):
        """Test more complex graph"""
        costs = [0, 5, 2, 3, 4]
        edges = [[0, 1, 2], [0, 2, 8], [1, 3, 7], [2, 3, 1], [3, 4, 3], [1, 4, 15]]
        expected = [0, 2, 8, 11, 17]
        self.assertEqual(compute_cost_dijkstra(costs, edges, 0), expected)
        self.assertEqual(compute_cost_dijkstra_heapq(costs, edges, 0), expected)

    def test_heapq_vs_bisect(self):
        """Verify heapq and bisect Dijkstra variants produce same results"""
        test_cases = [
            ([1, 2, 3], [[0, 1, 4], [1, 2, 5], [0, 2, 10]]),
            (
                [0, 5, 2, 3, 4],
                [[0, 1, 2], [0, 2, 8], [1, 3, 7], [2, 3, 1], [3, 4, 3], [1, 4, 15]],
            ),
            ([0, 1, 1], [[0, 1, 5], [0, 1, 3]]),
            ([0, 2, 2], [[0, 1, 10], [0, 1, 4], [0, 1, 7]]),
        ]
        for costs, edges in test_cases:
            result_bisect = compute_cost_dijkstra(costs, edges, 0)
            result_heapq = compute_cost_dijkstra_heapq(costs, edges, 0)
            self.assertEqual(
                result_bisect,
                result_heapq,
                f"Mismatch for costs={costs}, edges={edges}",
            )

    def test_duplicate_edges_two(self):
        """Test that minimum edge weight is selected when two edges exist"""
        costs = [0, 1, 1]
        edges = [[0, 1, 5], [0, 1, 3]]
        expected = [0, 3, -1]
        self.assertEqual(compute_cost_dijkstra(costs, edges, 0), expected)
        self.assertEqual(compute_cost_dijkstra_heapq(costs, edges, 0), expected)
        self.assertEqual(compute_cost_mine(costs, edges, 0), expected)

    def test_duplicate_edges_three(self):
        """Test that minimum edge weight is selected when multiple edges exist"""
        costs = [0, 2, 2]
        edges = [[0, 1, 10], [0, 1, 4], [0, 1, 7]]
        expected = [0, 4, -1]
        self.assertEqual(compute_cost_dijkstra(costs, edges, 0), expected)
        self.assertEqual(compute_cost_dijkstra_heapq(costs, edges, 0), expected)
        self.assertEqual(compute_cost_mine(costs, edges, 0), expected)

    def test_unreachable_node(self):
        """Test that unreachable nodes return -1"""
        costs = [0, 1]
        edges = [[0, 0, 5]]
        expected = [0, -1]
        self.assertEqual(compute_cost_dijkstra(costs, edges, 0), expected)
        self.assertEqual(compute_cost_dijkstra_heapq(costs, edges, 0), expected)
        self.assertEqual(compute_cost_mine(costs, edges, 0), expected)

    def test_single_node(self):
        """Test with single node"""
        costs = [5]
        edges = []
        expected = [0]
        self.assertEqual(compute_cost_dijkstra(costs, edges, 0), expected)
        self.assertEqual(compute_cost_dijkstra_heapq(costs, edges, 0), expected)
        self.assertEqual(compute_cost_mine(costs, edges, 0), expected)

    def test_mine_fails_longer_relay_path(self):
        """compute_cost_mine misses shorter path 0->4->1->3 (cost 47 vs 63)"""
        costs = [8, 6, 7, 3, 6]
        edges = [
            [1, 1, 14],
            [3, 0, 20],
            [1, 3, 19],
            [3, 3, 1],
            [1, 1, 9],
            [0, 4, 4],
            [4, 1, 12],
            [2, 1, 15],
            [0, 2, 16],
        ]
        expected = [0, 22, 16, 47, 4]
        # Both Dijkstra variants pass
        self.assertEqual(compute_cost_dijkstra(costs, edges, 0), expected)
        self.assertEqual(compute_cost_dijkstra_heapq(costs, edges, 0), expected)
        # compute_cost_mine returns [0, 22, 16, 63, 4] — node 3 is wrong
        self.assertNotEqual(compute_cost_mine(costs, edges, 0), expected)

    def test_mine_fails_indirect_cheaper_path(self):
        """compute_cost_mine misses shorter path to node 2 (cost 43 vs 49)"""
        costs = [1, 8, 1, 8, 2, 8, 1]
        edges = [
            [4, 5, 7],
            [6, 0, 14],
            [6, 2, 15],
            [3, 5, 5],
            [5, 2, 3],
            [1, 5, 19],
            [2, 3, 17],
            [6, 5, 14],
            [0, 3, 19],
            [2, 0, 20],
            [6, 3, 1],
            [0, 1, 11],
            [3, 1, 9],
        ]
        expected = [0, 11, 43, 19, -1, 32, -1]
        # Both Dijkstra variants pass
        self.assertEqual(compute_cost_dijkstra(costs, edges, 0), expected)
        self.assertEqual(compute_cost_dijkstra_heapq(costs, edges, 0), expected)
        # compute_cost_mine returns [0, 11, 49, 19, -1, 32, -1] — node 2 is wrong
        self.assertNotEqual(compute_cost_mine(costs, edges, 0), expected)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "main":
        main()
    else:
        unittest.main()
