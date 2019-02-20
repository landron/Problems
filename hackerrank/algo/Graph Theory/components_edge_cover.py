#!/bin/python3
'''
    Graphs
        connected component edge cover

    https://www.hackerrank.com/challenges/torque-and-development

    pylint, flake8

    tag_graph
'''


def merge_components(component, node1, node2):
    '''
        keep components as a list:
        - if None => no edge found yet
        - if len == 1 => it indirects to the ID node of the component
        - else: it contains all the nodes of the component

        when components are merged, we do not update all the individual nodes
    '''
    assert component[node1-1] and component[node2-1]

    def merge_components_base(component, node1, node2):
        assert node1 != node2
        assert len(component[node1-1]) > 1
        assert len(component[node2-1]) > 1

        size1 = len(component[node1-1])
        size2 = len(component[node2-1])
        if size1 < size2 or (size1 == size2 and node1 > node2):
            node1, node2 = node2, node1

        component[node1-1].extend(component[node2-1])
        component[node2-1] = [node1]

    def merge_components_secondary(component, node1, node2):
        assert len(component[node1-1]) == 1 or len(component[node2-1]) == 1
        assert len(component[node1-1]) != 1 or len(component[node2-1]) != 1

        size1 = len(component[node1-1])
        size2 = len(component[node2-1])
        if size1 < size2 or (size1 == size2 and node1 > node2):
            node1, node2 = node2, node1

        # node_id = component[node2-1][0]
        node_id = get_final_component_node(component, node2)
        if node_id == node1:
            return False
        merge_components_base(component, node1, node_id)
        component[node2-1] = [node_id]

        return True

    component1 = component[node1-1]
    component2 = component[node2-1]

    if len(component1) > 1:
        if len(component2) > 1:
            merge_components_base(component, node1, node2)
            # assert component[node1-1] == component[node2-1]
        else:
            if not merge_components_secondary(component, node1, node2):
                return False
    elif len(component2) > 1:
        if not merge_components_secondary(component, node1, node2):
            return False
    else:
        node_id = get_final_component_node(component, node1)
        if not merge_components_secondary(component, node_id, node2):
            return False
        component[node1-1] = component[node2-1]

    return True


def get_final_component_node(component, node):
    '''
        get the final component node (ID) of a chain

        see merge_components for how we keep those IDs
    '''
    assert len(component[node-1]) == 1
    while len(component[node-1]) == 1:
        node = component[node-1][0]
    return node


def get_edge_cover(nodes_no, edges, trace):
    '''
        get the edge cover, but keep the components

        see merge_components for how we keep the components
    '''
    edges_cover_no = 0
    component = [None] * nodes_no

    for i in edges:
        node1 = i[0]
        node2 = i[1]
        if not component[node1-1]:
            node1, node2 = node2, node1

        component1 = component[node1-1]
        component2 = component[node2-1]

        if component1:
            if component2:
                if not merge_components(component, node1, node2):
                    continue
            else:
                node_id = node1 if len(component1) > 1 else\
                          get_final_component_node(component, node1)
                component[node_id-1].append(node2)
                component[node2-1] = [node_id]
        else:
            assert not component2

            if node1 > node2:
                node1, node2 = node2, node1
            component[node1-1] = [node1, node2]
            component[node2-1] = [node1]

        edges_cover_no += 1
        if trace:
            print(i, component)

    components_no = 0
    for i in range(nodes_no):
        if component[i] and len(component[i]) == 1:
            continue
        components_no += 1
    assert components_no <= nodes_no

    return (components_no, edges_cover_no)


def get_total_cost(nodes_no, edges, cost_by_component, cost_by_edge,
                   trace=False):
    '''
        get total cost of the edge cover that keeps the components
    '''
    components_no, edges_cover_no = get_edge_cover(nodes_no, edges, trace)

    if trace:
        print(components_no, edges_cover_no)

    return components_no*cost_by_component + edges_cover_no*cost_by_edge


def get_optimal_cost(nodes_no, edges, cost_by_component, cost_by_edge):
    '''
        get optimal cost between for components with or without adding edges
    '''
    if cost_by_component <= cost_by_edge:
        return nodes_no * cost_by_component
    return get_total_cost(nodes_no, edges, cost_by_component, cost_by_edge)


def parse_input_with(input_func):
    '''
        parse input with the given function
    '''
    queries_no = int(input_func().strip())
    for _ in range(queries_no):
        nodes_no, edges_no, cost_lib, cost_road =\
            (int(i) for i in input_func().strip().split())
        edges = []
        for _ in range(edges_no):
            edges.append([int(i) for i in input_func().strip().split()])

        cost = get_optimal_cost(nodes_no, edges, cost_lib, cost_road)
        print(cost)


def parse_input():
    '''
        parse input in the HackerRank format
    '''
    parse_input_with(input)


def parse_big_test():
    '''
        parse (failing) file test from HackerRank
    '''
    fptr = open('input02.txt', 'r')
    parse_input_with(fptr.readline)


def tests():
    '''
        unit tests, assertions
    '''
    assert get_total_cost(3, [(1, 2), (3, 1), (2, 3)], 2, 1) == 4
    assert get_total_cost(6, [(1, 3), (3, 4), (2, 4), (1, 2), (2, 3), (5, 6)],
                          2, 5) == 24
    assert get_optimal_cost(6, [(1, 3), (3, 4), (2, 4), (1, 2), (2, 3),
                                (5, 6)], 2, 5) == 12
    assert get_optimal_cost(7, [(1, 2), (3, 1), (1, 6), (2, 3), (5, 4),
                                (5, 7)], 3, 2) == 16
    assert get_optimal_cost(8, [(1, 2), (3, 1), (1, 7), (2, 3), (5, 6),
                                (6, 8)], 3, 2) == 19

    assert get_optimal_cost(3, [(1, 2), (3, 1), (2, 3), (1, 3)], 2, 1) == 4
    assert get_optimal_cost(3, [(1, 2)], 2, 1) == 5
    assert get_optimal_cost(4, [(1, 2), (2, 3), (1, 4), (3, 4)], 2, 1) == 5
    assert get_optimal_cost(4, [(1, 2), (4, 3)], 2, 1) == 6
    assert get_optimal_cost(4, [(1, 2), (4, 3), (2, 4)], 2, 1) == 5

    #   errors solved
    assert get_optimal_cost(5, [(1, 2), (4, 3), (2, 4), (2, 5)], 2, 1) == 6
    assert get_optimal_cost(5, [(1, 2), (4, 3), (1, 3), (4, 5)], 2, 1) == 6


def main():
    '''main'''
    tests()

    # parse_input()
    # parse_big_test()


if __name__ == '__main__':
    main()
