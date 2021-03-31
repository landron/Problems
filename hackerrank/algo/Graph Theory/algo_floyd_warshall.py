"""
    https://www.hackerrank.com/challenges/floyd-city-of-blinding-lights/problem
        It didn't pass with Python 3, but it did with PyPy3.

    Reference
        Floyd–Warshall algorithm
            https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
        for further small optimizations:
            https://www.hackerrank.com/challenges/floyd-city-of-blinding-lights/forum/comments/221588

    tag_floyd

    pylint, flake8
"""
NO_PATH = -1


def init_graph(nodes_no):
    '''
        initialize edges weight in the graph
        NO_PATH = special value different from any weight
                (infinite is even easier/better)
    '''
    edges = [[NO_PATH] * nodes_no for i in range(nodes_no)]
    for i in range(nodes_no):
        edges[i][i] = 0
    return edges


def print_graph(edges):
    '''debugging function'''
    for i in edges:
        for j in i:
            print("{0:3} ".format(j), end='')
        print()


def floyd_warshall(edges):
    '''
        Reference
            see "Pseudocode for this basic version follows"
            https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm

        O(N^3)
    '''
    distances = [w[:] for w in edges]

    nodes_no = len(edges)
    for k in range(nodes_no):
        for i in range(nodes_no):
            if distances[i][k] == NO_PATH:
                continue
            for j in range(nodes_no):
                if NO_PATH != distances[k][j]:
                    new = distances[i][k] + distances[k][j]
                    if NO_PATH == distances[i][j] or new < distances[i][j]:
                        distances[i][j] = new
    # print_graph(distances)
    return distances


def parse_input():
    '''
        read input and solve the problem as defined on HackerRank

    sample input:
4 5
1 2 5
1 4 24
2 4 6
3 4 4
3 2 7
3
1 2
3 1
1 4
    '''
    # pylint: disable=invalid-name

    road_nodes, road_edges = map(int, input().split())

    road_from = [0] * road_edges
    road_to = [0] * road_edges
    road_weight = [0] * road_edges

    for i in range(road_edges):
        road_from[i], road_to[i], road_weight[i] = map(int, input().split())

    edges = init_graph(road_nodes)
    for i in range(road_edges):
        edges[road_from[i]-1][road_to[i]-1] = road_weight[i]
    distances = floyd_warshall(edges)

    q = int(input())

    for _ in range(q):
        xy = input().split()

        x = int(xy[0])

        y = int(xy[1])

        print(distances[x-1][y-1])


def debug_validations():
    """
        unit tests
    """
    # sample input 1
    edges = init_graph(5)
    edges[0][1] = 5
    edges[0][4] = 3
    edges[1][2] = 1
    edges[4][2] = 2
    edges[3][0] = 4
    distances = floyd_warshall(edges)
    assert distances[3][2] == 9
    assert distances[1][4] == NO_PATH
    assert distances[4][2] == 2

    # sample input 2
    edges = init_graph(4)
    edges[0][1] = 5
    edges[0][3] = 24
    edges[1][3] = 6
    edges[2][3] = 4
    edges[2][1] = 7
    distances = floyd_warshall(edges)
    assert distances[0][1] == 5
    assert distances[2][0] == NO_PATH
    assert distances[0][3] == 11


if __name__ == "__main__":
    debug_validations()
    # parse_input()
