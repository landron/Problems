'''
    http://www.hackerrank.com/challenges/bfsshortreach
        Breadth First Search: Shortest Reach
    Direct Dijkstra application.
    tag_dijkstra

    Version 2016.05.08

    >pylint --version
        No config file found, using default configuration
        pylint 1.5.5,
        astroid 1.4.5
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10
'''

def find_shortest(nodes_no, edges, start):
    '''using Dijkstra to find the minimum distance from the 'start' node
        to all the others
    '''
    assert len(edges) != 0

    distance = {}
    for node in range(nodes_no):
        distance[node] = -1
    distance[start] = 0
    for node in edges[start]:
        distance[node] = 6

    visited = {start}
    unvisited = [start]
    while unvisited:
        current = unvisited.pop(0)
        for node in edges[current]:
            # print(edges[current])
            if node not in visited:
                dist = distance[current] + 6
                if distance[node] == -1:
                    distance[node] = dist
                elif distance[node] > dist:
                    distance[node] = dist
                visited.add(node)
                unvisited.append(node)

    return distance

def read_and_solve_func(input_func):
    '''hackerrank input interface'''
    tests_no = int(input_func().strip())
    for _ in range(tests_no):
        (nodes, edges_no) = [int(arr_temp) for arr_temp in input_func().strip().split(' ')]
        edges = {}
        for i in range(nodes):
            edges[i] = {}
        for _ in range(edges_no):
            (src, dest) = [int(arr_temp) for arr_temp in input_func().strip().split(' ')]
            assert src > 0 and dest > 0
            edges[src-1][dest-1] = True
            edges[dest-1][src-1] = True
        start = int(input_func().strip())-1
        assert start >= 0

        distances = find_shortest(nodes, edges, start)
        for i in range(nodes):
            if i != start:
                print(distances[i], '', end='')
        print()

def read_and_solve():
    '''hackerrank input interface'''
    read_and_solve_func(input)

def read_and_solve_file(file_name):
    '''hackerrank test case'''
    file = open(file_name, 'r')
    read_and_solve_func(file.readline)

def debug_validations():
    '''unit testing'''
    pass

def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()
    read_and_solve_file("in02.txt")

if __name__ == "__main__":
    main()
