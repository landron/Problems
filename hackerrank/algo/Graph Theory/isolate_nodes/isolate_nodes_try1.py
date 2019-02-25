#!/bin/python3
'''
    https://www.hackerrank.com/challenges/matrix/problem
        - nodes start from 0 -> n-1
        - all connected by n-1 edges ;)

    Version 2019.02.23: 4/12 (4 failed, 5 time-outs)
    Version 2019.02.24: 5/12 (7 time-outs)
                        with get_solution_try_all

    tag_hard !?
    tag_graph
        combination of: BFS, connected components
'''
import bisect


def search(alist, item):
    '''
        Locate the leftmost value exactly equal to item
        https://stackoverflow.com/questions/38346013/binary-search-in-a-python-list
        about 3 times faster than "item in alist"
    '''
    found = bisect.bisect_right(alist, item)
    if found < len(alist)+1 and alist[found-1] == item:
        return found-1
    return -1


def get_max_cost(nodes, to_eliminate):
    '''
        a rough estimate of the maximal cost:
            leaving nodes to eliminate without connection
    '''
    cost = 0
    for _, node in enumerate(to_eliminate):
        adj_list = nodes[node]
        for _, val in enumerate(adj_list):
            cost += val[1]
    return cost


def eliminate_safe_edges(nodes, edges, to_eliminate):
    '''
        edges to safe leaves are not necessary
    '''
    def is_safe_leaf(node, nodes, to_eliminate):
        assert nodes[node]
        if len(nodes[node]) > 1:
            return False
        return -1 == search(to_eliminate, node)

    def remove_edge(node1, node2, nodes):
        def remove_edge_base(src, dest, nodes):
            for i, val in enumerate(nodes[src]):
                if val[0] == dest:
                    del nodes[src][i]
                    return True
            return False
        removed = remove_edge_base(node1, node2, nodes)
        assert removed
        removed = remove_edge_base(node2, node1, nodes)
        assert removed

    changed = True
    while changed:
        changed = False
        size = len(edges)
        for i, edge in enumerate(reversed(edges)):
            if is_safe_leaf(edge[0], nodes, to_eliminate) or\
               is_safe_leaf(edge[1], nodes, to_eliminate):
                del edges[size-i-1]
                remove_edge(edge[0], edge[1], nodes)
                changed = True


def minimize_cost_brute_force(nodes, edges, to_eliminate, cost_min, trace):
    '''
        Purpose
            isolate the nodes to eliminate

        brute force
            - get the minimal edge:
                if nodes are eliminated/different components, keep this one
            - get next edge until all are separated

        Obsolete: too slow
    '''
    # pylint: disable=too-many-statements

    def get_components(nodes, ignored_edges):
        component = [i for i, _ in enumerate(nodes)]
        visited = [False] * len(nodes)
        for i, adj_list in enumerate(nodes):
            if visited[i] or not adj_list:
                continue
            bfs = [i]
            while bfs:
                node = bfs.pop(0)
                visited[node] = True
                component[node] = i
                for adjacent in nodes[node]:
                    if visited[adjacent[0]]:
                        continue
                    edge = (node, adjacent[0])
                    if node > adjacent[0]:
                        edge = (adjacent[0], node)
                    if edge in ignored_edges:
                        continue
                    bfs.append(adjacent[0])

        return component

    def are_nodes_connected(component, nodes):
        known_components = {}
        for i in nodes:
            if component[i] in known_components:
                return True
            known_components[component[i]] = True
        return False

    def improve_components(component_old, nodes, to_remove, to_eliminate):
        '''
            any improvement with the newly added edge ?
        '''
        component_new = get_components(nodes, to_remove)
        for _, node in enumerate(to_eliminate):
            if component_new[node] != component_old[node]:
                return component_new
        return None

    def improve_components_by_no(components_no, nodes, to_remove,
                                 to_eliminate):
        '''
            any improvement with the newly added edge ?
        '''
        def get_components_no(component, to_eliminate):
            component_to_separate = {}
            count = 0
            for _, node in enumerate(to_eliminate):
                if component[node] not in component_to_separate:
                    component_to_separate[component[node]] = True
                    count += 1
            return count
        component_new = get_components(nodes, to_remove)
        assert component_new
        no2 = get_components_no(component_new, to_eliminate)

        if 0:  # unfinished business
            if components_no > no2:
                print(components_no, no2)
                print(component_new)
            assert components_no <= no2

        return None if components_no == no2 else (component_new, no2)

    def get_solution_lucky(  # pylint: disable=unused-variable
            nodes, edges, to_eliminate):
        to_remove = {}
        component = [0] * len(nodes)

        for _, edge in enumerate(edges):
            assert edge[0] < edge[1]
            to_remove[(edge[0], edge[1])] = edge[2]
            component_new = improve_components(component, nodes, to_remove,
                                               to_eliminate)
            if not component_new:
                del to_remove[(edge[0], edge[1])]
                continue
            component = component_new

            if trace:
                # print(edge, component)
                pass
            if not are_nodes_connected(component, to_eliminate):
                break

        cost = 0
        for _, key in enumerate(to_remove):
            cost += to_remove[key]
        return cost

    def get_solution_try_all(nodes, edges, to_eliminate, cost_min,
                             trace):  # pylint: disable=unused-argument
        to_remove = {}
        component_next = improve_components_by_no(
            0, nodes, to_remove, to_eliminate)
        _, component_no_init = component_next

        for i, first in enumerate(edges):
            if first[2] > cost_min:
                break

            component_no = component_no_init
            cost = 0
            solution = []

            j = i
            while j < len(edges):
                edge = edges[j]
                assert edge[0] < edge[1]
                to_remove[(edge[0], edge[1])] = edge[2]
                component_next = improve_components_by_no(
                    component_no, nodes, to_remove, to_eliminate)
                if not component_next:
                    del to_remove[(edge[0], edge[1])]
                    j += 1
                    continue

                component_new, component_no_with = component_next
                assert component_new

                cost += edge[2]
                finish = cost > cost_min
                if not finish:
                    finish = not are_nodes_connected(
                        component_new, to_eliminate)
                    if finish:
                        cost_min = cost

                if finish:
                    cost -= edge[2]
                    del to_remove[(edge[0], edge[1])]

                    if not solution:
                        break
                    j, component_no = solution.pop()
                    edge = edges[j]
                    del to_remove[(edge[0], edge[1])]
                else:
                    solution.append((j, component_no))
                    component_no = component_no_with

                j += 1

        return cost_min

    edges.sort(key=lambda e: e[2])

    # get_solution_lucky is good enough for the simple tests()
    # cost = get_solution_lucky(nodes, edges, to_eliminate)
    cost = get_solution_try_all(nodes, edges, to_eliminate, cost_min, trace)
    if cost_min > cost:
        cost_min = cost

    return cost_min


def minimize_cost(nodes, edges, to_eliminate, cost_min, trace):
    '''
        Purpose
            isolate the nodes to eliminate

        Idea 1
            - take one, do BFS and try to find another
            - if found: eliminate the minimal edge
            problem: cannot be sure if it goes through all the combinations

        Idea 2
            brute force
            - get the minimal edge:
                if nodes are eliminated/different components, keep this one
            - get next edge until all are separated
    '''
    return minimize_cost_brute_force(nodes, edges, to_eliminate, cost_min,
                                     trace)


def isolate_nodes(edges, to_eliminate, trace=False):
    '''
        all N nodes connected + N-1 edges => no cycles, so unique paths
        (there must be a theorem out there)
    '''
    # problem's conditions
    assert len(edges)+1 >= 2
    assert len(to_eliminate) >= 2
    nodes_no = len(edges) + 1

    to_eliminate.sort()

    cost = 0

    # 1. first, simplify to eliminate some nodes already

    # 1.1 edge between two nodes to eliminate => eliminate it!
    size = len(edges)
    for i, edge in enumerate(reversed(edges)):
        found1 = -1 < search(to_eliminate, edge[0])
        found2 = -1 < search(to_eliminate, edge[1])
        if found1 and found2:
            cost += edge[2]
            del edges[size-i-1]

    # each edge has the node in ascendent order (it will be used later)
    for _, edge in enumerate(edges):
        if edge[0] > edge[1]:
            edge[0], edge[1] = edge[1], edge[0]

    # 1.2 adjacency list

    nodes = [[] for _ in range(nodes_no)]
    for _, edge in enumerate(edges):
        nodes[edge[0]].append((edge[1], edge[2]))
        nodes[edge[1]].append((edge[0], edge[2]))

    # 1.3 nodes left unconnected
    size = len(to_eliminate)
    for i, val in enumerate(reversed(to_eliminate)):
        if not nodes[val]:
            del to_eliminate[size-i-1]

    if not to_eliminate or len(to_eliminate) == 1:
        return cost

    # 1.4 eliminate some noise
    eliminate_safe_edges(nodes, edges, to_eliminate)

    # 2. get a first evaluation of the remaining cost and try to minimize it

    cost_min = minimize_cost(nodes, edges, to_eliminate,
                             get_max_cost(nodes, to_eliminate), trace)

    return cost+cost_min


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

    # 645 vs 610
    cost_min = isolate_nodes(edges, to_eliminate, True)
    print(cost_min)


def parse_big_test():
    '''
        parse (failing) file test from HackerRank
    '''
    fptr = open('input02.txt', 'r')
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
    assert isolate_nodes([[1, 0, 3], [1, 2, 1]], [0, 2]) == 1
    assert isolate_nodes([[1, 0, 3], [1, 2, 1], [0, 3, 1]], [0, 2]) == 1
    assert isolate_nodes([[1, 0, 1], [0, 2, 2], [0, 3, 3]], [1, 2, 3]) == 3
    assert isolate_nodes([[1, 0, 1], [0, 2, 2], [0, 3, 3]], [1, 2, 0]) == 3
    assert isolate_nodes([[1, 0, 1], [0, 2, 2], [0, 3, 3]], [1, 3, 0]) == 4

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
    # result = isolate_nodes([[1, 0, 1], [0, 2, 2], [0, 3, 3]],
    #                        [1, 2, 3], True)
    # print(result)

    # parse_input()
    parse_big_test()


if __name__ == '__main__':
    main()
