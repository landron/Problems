#!/bin/python3
'''
    https://www.hackerrank.com/challenges/balanced-forest
        "Interview Preparation Kit"

    nodes: 1..n

    Version 02.03.2019:     3/8 (3 failures, 2 time-outs)
    Version 02.03.2019, 2:  5/8 (1 failure, 2 time-outs)

    tag_python_class
    tag_python_class_copy
        https://stackoverflow.com/questions/35470379/proper-idiomatic-way-to-implement-clone-method-in-python-class
    tag_tree

    tag_hard

    flake8, pylint
'''


def calculate_tree(node, costs, adj, exclude):
    '''
        calculate the cost of the subtree
    '''
    cost = costs[node-1]
    queue = [node]
    while queue:
        node = queue.pop(0)
        if not adj[node-1]:
            continue
        for i in adj[node-1]:
            if i not in exclude:
                queue.append(i)
                cost += costs[i-1]
    return cost


class Position:
    '''
        position inside tree

        used for edge elimination, so it does not retain the "leaves"
            in the queue
    '''

    def __init__(self, adj_list):
        # immutable
        self.adj = adj_list
        assert adj_list[0]

        self.node = 1
        self.idx = 0
        self.to_process = []

    def __str__(self):
        if not self.node:
            return "invalid"
        description = "("
        description += str(self.node)
        description += ", "
        if self.adj[self.node-1]:
            description += str(self.idx)
            description += ", "
        description += str(self.to_process)
        description += ")"
        return description

    def copy(self):
        '''
            clone the current node
        '''
        clone = Position(self.adj)
        clone.node = self.node
        clone.idx = self.idx
        clone.to_process = self.to_process[:]
        return clone

    __copy__ = copy

    def __bool__(self):
        '''
            is the current iterator valid ?
        '''
        return self.node is not None

    def increment(self):
        '''
            increment the current position
        '''
        assert self
        assert self.node and self.node <= len(self.adj)
        # print("increment", self)

        node = self.adj[self.node-1][self.idx]
        if self.adj[node-1]:
            self.to_process.append(node)

        self.idx += 1
        if self.idx < len(self.adj[self.node-1]):
            return

        # get another node

        if self.to_process:
            self.node = self.to_process.pop(0)
            assert self.adj[self.node-1], "it should not have been added"
            self.idx = 0
        else:
            self.node = None

    def edge_to(self):
        '''
            get the other end of the current edge
        '''
        # print("edge_to", self)
        assert self.node <= len(self.adj)
        assert self.adj[self.node-1]
        return self.adj[self.node-1][self.idx]


class Components:
    '''track the 3 components'''

    def __init__(self, costs, trace):
        # the roots of the subtrees: this is all we need to keep!
        self.component = [0] * 3
        self.component[0] = 1

        # immutable(s)
        self.costs = costs
        self.trace = trace

    def __str__(self):
        description = "("
        for i in self.component:
            description += str(i)
            description += ', '
        description = description[:-2]
        description += ")"
        return description

    def get_components_no(self):
        '''get the number of components'''
        count = 0
        for i in self.component:
            if not i:
                break
            count += 1
        return count

    def new_component(self, node):
        '''add the node as a new component'''
        assert self.component[0]
        for i in self.component:
            assert node != i

        pos = None
        for i, val in enumerate(self.component):
            if not val:
                pos = i+1
                break
        # no more open spaces
        if not pos:
            return False
        self.component[pos-1] = node

        if self.trace:
            print("new_component", node, self)

        return True

    def remove_node(self, node):
        '''remove this node from components'''
        pos = None
        for i, val in enumerate(self.component):
            if node == val:
                pos = i+1
                break
        self.component[pos-1] = 0
        if self.trace:
            print("remove_node", node, self)

    def calculate_solution(self, adj_list):
        '''
            calculate the existing solution

            one empty component is acceptable = the new node
        '''
        exclude = set(self.component)
        if len(exclude) != 3:
            return -1

        cost = [0] * 3
        for i in range(3):
            if self.component[i]:
                cost[i] = calculate_tree(self.component[i], self.costs,
                                         adj_list, exclude)
        cost.sort()
        if self.trace:
            print("calculate_solution", self, cost)
        if cost[1] == cost[2]:
            solution = cost[1] - cost[0]
            if self.trace:
                print("calculate_solution, found", solution)
            return solution

        return -1


def balanced_forest_rec(costs, position, rec_data):
    '''
        dynamic programming solution to complete all the possibilities
    '''
    assert rec_data.to_cut

    component = rec_data.component
    adj_list = position.adj
    if not position:
        return component.calculate_solution(adj_list)

    node_edge = position.edge_to()

    current = position.copy()
    current.increment()

    cost = -1

    # calculate cost without the current edge

    rec_data.to_cut -= 1
    if component.new_component(node_edge):
        if rec_data.to_cut:
            cost = balanced_forest_rec(costs, current, rec_data)
        else:
            cost = component.calculate_solution(adj_list)
        component.remove_node(node_edge)

    rec_data.to_cut += 1

    # calculate cost with the current edge

    cost_with = balanced_forest_rec(costs, current, rec_data)
    if cost_with != -1:
        if cost == -1 or cost > cost_with:
            cost = cost_with

    return cost


def balanced_forest(costs, edges, trace=False):
    '''
        cut the given tree in three parts:
        - two are equal
        - the third has cost such as adding another node equals
            the other two components
        - this added node must have a minimal cost
    '''
    assert len(costs) == len(edges) + 1

    for i in edges:
        if i[0] > i[1]:
            i[0], i[1] = i[1], i[0]
    edges.sort(key=lambda e: e[0])

    if trace:
        print(edges)

    # adjacency list

    def make_adjancey_list(edges):
        nodes_no = len(edges) + 1

        adj = [None] * nodes_no
        for i in edges:
            def add_to(adj, node1, node2):
                if not adj[node1-1]:
                    adj[node1-1] = set([node2])
                else:
                    adj[node1-1].add(node2)
            add_to(adj, i[0], i[1])
            add_to(adj, i[1], i[0])

        # eliminate "back" edges to have a one-direction tree:
        #   from root to the leaves

        queue = [1]
        while queue:
            node = queue.pop()
            if not adj[node-1]:
                continue
            for i in adj[node-1]:
                queue.append(i)
                adj[i-1].remove(node)

        # now back to list because we need indexed access

        for i in range(nodes_no):
            adj[i] = list(adj[i])

        return adj

    adj = make_adjancey_list(edges)

    # define recursive data

    rec_data = lambda: None  # noqa: E731
    rec_data.component = Components(costs, trace)
    rec_data.to_cut = 2
    # not used yet
    rec_data.solution = 0
    for i in costs:
        rec_data.solution += i

    # do the work

    cost_min = balanced_forest_rec(costs, Position(adj), rec_data)

    return cost_min


def parse_with(input_func, output_func):
    '''
        parse the HackerRank input
    '''
    no_tests = int(input_func().strip())
    for _ in range(no_tests):
        nodes_no = int(input_func().strip())
        costs = [int(i) for i in input_func().strip().split()]
        edges = []
        for _ in range(nodes_no-1):
            edges.append([int(i) for i in input_func().strip().split()])

        cost = balanced_forest(costs, edges)
        output_func(cost)


def parse_big_test():
    '''
        parse some big file HackerRank input

        correct: -1 10 13 5 297
        vs
        me: -1 -1 13 5 -1
    '''
    fptr = open('input01.txt', 'r')
    parse_with(fptr.readline, print)


def tests():
    '''
        unit tests
    '''

    # problem samples
    assert balanced_forest([15, 12, 8, 14, 13],
                           [[1, 2], [1, 3], [1, 4], [4, 5]]) == 19
    assert balanced_forest([1, 2, 2, 1, 1],
                           [[1, 2], [1, 3], [3, 5], [4, 1]]) == 2
    assert balanced_forest([1, 3, 5], [[1, 2], [1, 3]]) == -1

    # missed tests
    assert balanced_forest(
                [100, 100, 99, 99, 98, 98],
                [[1, 3], [3, 5], [1, 2], [2, 4], [6, 4]]) == 297
    assert balanced_forest(
                [1, 1, 1, 18, 10, 11, 5, 6],
                [[1, 2], [1, 4], [2, 3], [1, 8],
                 [8, 7], [7, 6], [5, 7]]) == 10
    assert balanced_forest(
                [1, 1, 1, 18, 6, 5, 10, 11],
                [[1, 2], [1, 4], [2, 3], [1, 8],
                 [8, 7], [7, 6], [5, 6]]) == 10

    # result = balanced_forest(
    #             [1, 1, 1, 18, 10, 11, 5, 6],
    #             [[1, 2], [1, 4], [2, 3], [1, 8],
    #              [8, 7], [7, 6], [5, 7]], True)
    # print(result)


def main():
    '''main'''
    tests()
    # parse_big_test()

    # result = balanced_forest(
    #         [1, 1, 1, 18, 6, 5, 10, 11],
    #         [[1, 2], [1, 4], [2, 3], [1, 8],
    #          [8, 7], [7, 6], [5, 6]], True)
    # print(result)


if __name__ == '__main__':
    main()
