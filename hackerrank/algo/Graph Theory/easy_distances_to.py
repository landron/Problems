#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/ctci-bfs-shortest-reach/problem

    tag_graph, tag_bfs (Breadth-first search)
    tag_class_python, tag_class_graph

    pylint, flake8
'''


class Graph():
    '''
        Graph by adjancency list
    '''
    def __init__(self, nodes_no, edges=None):
        self.nodes_no = nodes_no
        self.edges = edges
        if not self.edges:
            self.edges = [[] for _ in range(nodes_no)]
        assert len(self.edges) == nodes_no

    def __str__(self):
        return str(self.edges)

    def connect(self, src, dest):
        '''connect the given nodes'''
        self.edges[src].append(dest)
        self.edges[dest].append(src)

    def get_distances(self, src):
        '''get the distances from this node to the rest of them'''
        queue = [src]
        distances = [0] * self.nodes_no

        while queue:
            curr = queue.pop(0)
            assert curr >= 0

            for i in self.edges[curr]:
                if not distances[i]:  # not visited
                    distances[i] = distances[curr] + 1
                    queue.append(i)

        # eliminate src & update with the weight of 6
        distances.pop(src)
        distances = [6*i if i > 0 else -1 for i in distances]
        return distances

    def find_all_distances(self, src):
        '''find all the distances from this node to the rest of them
            and also print them (in the hackerrank format)
        '''
        distances = self.get_distances(src)
        # print(distances)
        for i in distances:
            print(i, end=' ')
        print()


def tests():
    '''
        tests for the current problem
    '''
    test = Graph(2)
    assert test.get_distances(1) == [-1]

    test = Graph(4, [[1, 2], [0], [0], []])
    assert test.get_distances(0) == [6, 6, -1]

    test = Graph(3, [[], [2], [1]])
    assert test.get_distances(1) == [-1, 6]

    test = Graph(6, [[1, 4], [0, 2], [1, 3], [2], [0], []])
    assert test.get_distances(0) == [6, 12, 18, 6, -1]


if __name__ == '__main__':
    tests()
