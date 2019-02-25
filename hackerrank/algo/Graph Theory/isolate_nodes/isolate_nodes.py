#!/bin/python3
'''
    https://www.hackerrank.com/challenges/matrix/problem
        - nodes start from 0 -> n-1
        - all connected by n-1 edges ;)

    Version 2019.02.23: 4/12 (4 failed, 5 time-outs)
    Version 2019.02.24: 5/12 (7 time-outs)
                        with get_solution_try_all
    Version 2019.02.24: 6/12 (5 failed, 1 time-out)
                        with minimize_cost_by_maximizing_components
                        At this step, I looked into the discussions
                        for ideas. The algorithm was good, but there was
                        something with the implementation.
    Version 2019.02.25: 6/12 failed
    Version 2019.02.25: succeeded
                        all the needed data by component is
                            "does it contain a forbidden node ?"

    tag_hard !?
    tag_graph
        combination of: BFS, connected components

    tag_kruskal
        https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
        minimum spanning tree (forest): ... but Kruskal it is easy

        The idea is the same: expand components with the heaviest edges,
            so that they contain one forbidden node at most. Also, there
            are always forbidden-1 edges eliminated.

    flake8, pylint
'''


def maximize_components_old(nodes_no, edges, forbidden, trace):
    '''
        try to make components with maximal cost without more than one
            forbidden node each
    '''
    assert trace or not trace, "maybe unused"
    assert edges[0] == max(edges, key=lambda e: e[2]), "already sorted"
    assert nodes_no == len(edges)+1

    component = [None] * nodes_no
    for i in range(nodes_no):
        component[i] = lambda: None  # noqa: E731
        # component[i].forbidden = forbidden[i]
        component[i].forbidden = i+1 if forbidden[i] else 0
        # needed ?
        component[i].set = set([i])

    cost_min = 0
    count_eliminated = 0
    for node1, node2, cost in edges:
        # do not add a direct forbidden connection
        if component[node1].forbidden and component[node2].forbidden:
            # this validation solves nothing
            if component[node1].forbidden != component[node2].forbidden:
                cost_min += cost
                count_eliminated += 1
                continue
        else:
            component[node1].forbidden += component[node2].forbidden
        assert not component[node1].set & component[node2].set
        component[node1].set |= component[node2].set
        component[node2] = component[node1]

    if trace and 0:
        print("final components")
        for i, val in enumerate(component):
            if val:
                print(i, val.forbidden, val.set)

    def validate_after():
        count_forbidden = 0
        for _, i in enumerate(forbidden):
            if i:
                count_forbidden += 1
        # assert count_eliminated == count_forbidden-1
        if count_eliminated != count_forbidden-1:
            print(count_eliminated, count_forbidden)
        count_forbidden_components = 0
        for i in range(nodes_no):
            if component[i].forbidden:
                count_forbidden_components += 1
        print(nodes_no, count_forbidden, count_forbidden_components)
    if trace:
        validate_after()

    return cost_min


def maximize_components(nodes_no, edges, forbidden, trace):
    '''
        try to make components with maximal cost without more than one
            forbidden node each

        must be sure to update the "final" component

        final solution ... not so hard ?
            (but the problem set has no cycles or repetitions)
    '''
    assert edges[0] == max(edges, key=lambda e: e[2]), "already sorted"
    assert nodes_no == len(edges)+1

    component = [None] * nodes_no
    # 0 : component has a forbidden node
    # i+1 : a final component
    # other : "pointer" to some other component
    for i in range(nodes_no):
        component[i] = 0 if forbidden[i] else i+1

    def get_component(component, pos):
        while component[pos] and (pos+1) != component[pos]:
            pos = component[pos]-1
        return pos, component[pos]

    def update_component(component, node1, node2):
        pos1, component1 = get_component(component, node1)
        pos2, component2 = get_component(component, node2)

        if not component1 and not component2:
            return False
        if component1 == 0 or component2 == 0:
            component[pos1] = component[pos2] = 0
        else:
            component[pos2] = pos1+1
        return True

    cost_min = 0
    count_eliminated = 0
    for node1, node2, cost in edges:
        if not update_component(component, node1, node2):
            cost_min += cost
            count_eliminated += 1

    def debug_validate_after():  # no explicit parameters
        count_forbidden = 0
        for _, i in enumerate(forbidden):
            if i:
                count_forbidden += 1
        assert count_eliminated == count_forbidden-1
        # if count_eliminated != count_forbidden-1:
        #     print(count_eliminated, count_forbidden)
        count_forbidden_components = 0
        for i in range(nodes_no):
            _, comp = get_component(component, i)
            if not comp:
                count_forbidden_components += 1
        assert nodes_no == count_forbidden_components
        # print(nodes_no, count_forbidden, count_forbidden_components)
    if trace:
        debug_validate_after()

    return cost_min


def isolate_nodes(edges, to_eliminate, trace=False):
    '''
        Purpose
            get maximum cost cover without having two forbidden nodes
                in the same connected component
    '''
    nodes_no = len(edges)+1  # by definition

    forbidden = [False] * nodes_no
    for _, node in enumerate(to_eliminate):
        forbidden[node] = True

    edges.sort(key=lambda e: e[2], reverse=True)

    if 0:  # pylint: disable=using-constant-test
        def get_equal_seq(edges):
            equal_seq = []
            size = 0
            for i in range(1, len(edges)):
                if edges[i][2] == edges[i-1][2]:
                    size += 1
                elif size:
                    equal_seq.append((i-1-size, size+1))
                    size = 0
            if size:
                equal_seq.append((len(edges)-1-size, size+1))

            # trace
            #
            # if equal_seq:
            #     # print(edges, equal_seq)
            #     print(equal_seq)
            #     if 0:
            #         for _, val in enumerate(equal_seq):
            #             for i in range(val[0], val[1]):
            #                 print(i, end='')
            #             print()
            #         print()

            return equal_seq

        equal_seq = get_equal_seq(edges)
        # quickly becomes very big
        if 0 and trace and equal_seq:
            prod = 1
            for _, i in enumerate(equal_seq):
                prod *= i[1]
            print("Permutations number:", prod)

    return maximize_components(nodes_no, edges, forbidden, trace)


def parse_input_with(input_func):
    '''
        parse input with the given function (stdin, file)
    '''
    nodes_no, to_eliminate_no = (int(i) for i in input_func().strip().split())
    edges = []
    for _ in range(nodes_no-1):
        node1, node2, cost = (int(i) for i in input_func().strip().split())
        edges.append([node1, node2, cost])
    to_eliminate = []
    for _ in range(to_eliminate_no):
        to_eliminate.append(int(input_func().strip()))
    # print(edges, to_eliminate)

    cost_min = isolate_nodes(edges, to_eliminate, True)
    print(cost_min)


def parse_big_test():
    '''
        parse (failing) file test from HackerRank
    '''
    # fptr = open('input02.txt', 'r')  # 645 vs 610
    fptr = open('input03.txt', 'r')  # 1292630 vs 1310956 ; 1310956
    parse_input_with(fptr.readline)


def parse_input():
    '''
        parse input in the HackerRank format
    '''


def tests():
    '''
        unit tests
    '''

    # very simple
    assert isolate_nodes([[1, 0, 3]], [0, 1]) == 3
    assert isolate_nodes([[1, 0, 2], [1, 2, 1]], [0, 1, 2]) == 3
    assert isolate_nodes([[1, 0, 3], [1, 2, 1]], [0, 1]) == 3

    # simple
    assert isolate_nodes([[1, 0, 1], [0, 2, 2]], [1, 2]) == 1
    assert isolate_nodes([[1, 0, 3], [1, 2, 1]], [0, 2]) == 1
    assert isolate_nodes([[1, 0, 3], [1, 2, 1], [0, 3, 1]], [0, 2]) == 1
    assert isolate_nodes([[1, 0, 1], [0, 2, 2], [0, 3, 3]], [1, 2, 3]) == 3
    assert isolate_nodes([[1, 0, 1], [0, 2, 2], [0, 3, 3]], [1, 2, 0]) == 3
    assert isolate_nodes([[1, 0, 1], [0, 2, 2], [0, 3, 3]], [1, 3, 0]) == 4

    # complex
    assert isolate_nodes(
        [[1, 0, 3], [1, 2, 2], [1, 3, 4], [4, 3, 5], [4, 5, 1]], [1, 4]) == 4

    # problem samples
    assert isolate_nodes([[1, 0, 4], [1, 2, 3], [1, 3, 7], [0, 4, 2]],
                         [2, 3, 4]) == 5
    assert isolate_nodes([[1, 0, 5], [1, 2, 8], [1, 3, 4], [2, 4, 5]],
                         [2, 0, 4]) == 10
    assert isolate_nodes([[0, 3, 3], [1, 4, 4], [1, 3, 4], [2, 0, 5]],
                         [1, 3, 4]) == 8

    # new tests
    # result = isolate_nodes([[1, 0, 1], [0, 2, 2], [0, 3, 3]],
    #                        [1, 2, 3], True)
    # print(result)


def main():
    '''main'''
    tests()

    # result = isolate_nodes([[1, 0, 1], [0, 2, 2]], [1, 2], True)
    # print(result)

    # parse_input()
    # parse_big_test()


if __name__ == '__main__':
    main()
