#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/balanced-forest
        "Interview Preparation Kit"

    nodes: 1..n

    Version 02.03.2019:     5/8 (1 failure, 2 time-outs), version 1
    Version 04.03.2019:     precalculate tree, new algorithm
                                we can actually calculate the needed value
                                for a node
    Version 05.03.2019:     6/8 (2 time-outs)
                                save the parents in a set ?
    Version 05.03.2019, 2:  8/8 - keep the parents in a set
                            no need to update the tree of costs

    tag_python_class
    tag_tree
    tag_hard

    flake8, pylint
'''
import bisect


class TreeNode:
    '''
        a node in tree
    '''
    def __init__(self, node_id, parent, cost=0):
        self.nid = node_id
        self.parents = set()
        if parent:
            self.parents = parent.parents.copy()
            self.parents.add(parent.nid)
        self.adj_list = None
        self.cost = cost

    def get_description(self, with_adj_list, with_parent):
        '''
            printable description of this object

            with/without adjacency list
        '''
        def get_adj_list(adj):
            description = "("
            for i in adj:
                description += str(i.nid)
                description += ', '
            description = description[:-2]
            description += ")"
            return description

        description = "("
        if not self.parents:
            description += "root (1)"
            assert self.nid == 1, "only for test"
        else:
            if with_parent:
                description += str(self.parents)
                description += ' -> '
            description += str(self.nid)
        if self.cost:
            description += ', '
            description += str(self.cost)
        if with_adj_list:
            description += ', '
            if self.adj_list:
                description += get_adj_list(self.adj_list)
            else:
                description += 'leaf'
        description += ")"

        return description

    def __str__(self):
        return self.get_description(with_adj_list=True, with_parent=True)

    def add_child(self, node):
        '''add a child to this node'''
        assert self.nid in node.parents
        if self.adj_list:
            self.adj_list.append(node)
        else:
            self.adj_list = [node]


class Tree:
    '''
        a tree
    '''
    def __init__(self, edges, cost, trace=False):
        nodes_no = len(cost)
        assert nodes_no == len(edges) + 1

        self.root = TreeNode(1, None, cost[0])
        self.size = nodes_no
        # list of touples: (cost, root TreeNode, level: 0 based)
        self.cost_tree = []
        self.trace = trace

        adj_list = Tree.make_adjacency_list(edges)

        if adj_list[0]:
            queue = [self.root]
            while queue:
                node = queue.pop()
                assert adj_list[node.nid-1]
                for i in adj_list[node.nid-1]:
                    child = TreeNode(i, node, cost[i-1])
                    node.add_child(child)
                    if adj_list[i-1]:
                        queue.append(child)

        self.cost_tree = Tree.calculate_tree(self)

    def __str__(self):
        description = ''
        queue = [(0, self.root)]
        while queue:
            level, node = queue.pop()
            for i in range(level):
                description += '\t'
            # description += str(node)
            description += node.get_description(
                with_adj_list=False, with_parent=False)
            description += '\n'
            if node.adj_list:
                for i in node.adj_list:
                    queue.append((level+1, i))
        return description

    @staticmethod
    def get_list_ids(list_of_nodes):
        '''get the list of ids from the list of tree nodes'''
        nids = []
        for i in list_of_nodes:
            nids.append(i.nid)
        return nids

    @staticmethod
    def get_precalculated_printable(precalculated, only_costs=False):
        '''get the list of ids from the list of tree nodes'''
        to_show = []
        for i in precalculated:
            if only_costs:
                to_show.append(i[0])
            else:
                to_show.append((i[1].nid, i[0]))
        return to_show

    @staticmethod
    def make_adjacency_list(edges):
        '''make the adjacency list of the children'''
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
            adj[i] = list(adj[i]) if adj[i] else None

        return adj

    @staticmethod
    def calculate_tree(tree):
        '''calculate the subtree cost for each node:
           - first go down to the leaves
           - then calculate to the top
        '''
        def calculate_node(element, calculated):
            '''Returns extended list to calculate'''
            node, level = element
            idx = node.nid-1
            if calculated[idx]:
                return []
            if not node.adj_list:  # leaf
                calculated[idx] = (node.cost, node)
                return []

            cost = 0
            to_calculate = []
            for i in node.adj_list:
                if not calculated[i.nid-1]:
                    to_calculate.append((i, level+1))
                else:
                    cost += calculated[i.nid-1][0]
            if to_calculate:
                return to_calculate
            calculated[idx] = (cost + node.cost, node)
            return []

        to_process = [(tree.root, -1)]
        calculated = [None] * tree.size  # cost(node) >= 1
        while to_process:
            to_calculate = calculate_node(to_process[-1], calculated)
            if not to_calculate:
                to_process.pop()
            else:
                to_process.extend(to_calculate)

        if tree.trace:
            print(Tree.get_precalculated_printable(calculated,
                                                   only_costs=False))

        return calculated

    @staticmethod
    def evaluate_subtree(total_cost, subtree_cost):
        '''
            calculate c (minimal cost of the node to add) and
                the cost of the subtree to search for

            (I calculated all this on paper)
        '''
        if total_cost//2 < subtree_cost:
            return None
        if total_cost % 2 == 0 and total_cost//2 == subtree_cost:
            # it suffices to add another node with this cost
            return (subtree_cost, None, None)

        if total_cost % 3 == 0 and subtree_cost == total_cost//3:
            # must find 2 subtree_cost
            return (0, subtree_cost, None)
        if total_cost > 3*subtree_cost:
            cost = total_cost - 3*subtree_cost
            if cost % 2:
                return None
            cost //= 2
            # must find 2 "subtree_cost+cost"
            return (cost, subtree_cost+cost, None)
        cost = 3*subtree_cost - total_cost
        assert cost > 0
        # can find either subtree_cost-cost or subtree_cost
        return (cost, subtree_cost-cost, subtree_cost)

    def minimal_balanced_cost_correct(self):
        '''
            the core of this problem (algorithm):
            - for each node evaluate the possibility of being cut
            from the tree (as one of the three components)
        '''
        def find_subtree(cost_tree, cost_to_search, node_removed):
            '''
                bisect works for tuples:
                    https://stackoverflow.com/questions/45155345/python-search-a-sorted-list-of-tuples
            '''
            assert cost_to_search

            # first search for the value itself:
            #   not between the children or parents !
            found = bisect.bisect_left(cost_tree, (cost_to_search, ))
            for i in range(found, len(cost_tree)):
                node = cost_tree[i]
                if node[0] != cost_to_search:
                    break
                if node[1].nid == node_removed[1].nid or\
                   node_removed[1].nid in node[1].parents or\
                   node[1].nid in node_removed[1].parents:
                    continue
                return True

            # then search for the value updated between the parents !
            cost_updated = cost_to_search + node_removed[0]
            found = bisect.bisect_left(cost_tree, (cost_updated, ))
            for i in range(found, len(cost_tree)):
                node = cost_tree[i]
                if node[0] != cost_updated:
                    return False
                if node[1].nid not in node_removed[1].parents:
                    continue
                return True

            return False

        total_tree_cost = self.cost_tree[0][0]
        cost_min = total_tree_cost+1
        cost_tree = sorted(self.cost_tree, key=lambda t: t[0])
        if self.trace:
            print(Tree.get_precalculated_printable(cost_tree,
                                                   only_costs=False))
        for i in cost_tree:
            result = Tree.evaluate_subtree(total_tree_cost, i[0])
            if not result:
                continue
            cost, to_search_1, to_search_2 = result
            assert not to_search_1 or to_search_2 != to_search_1
            if self.trace:
                print("evaluate_subtree", i[1].nid, cost, to_search_1)

            if cost >= cost_min:
                continue
            if not to_search_1:
                cost_min = cost
                continue

            # if self.trace:
            #     print(Tree.get_precalculated_printable(cost_tree_u,
            #                                            only_costs=False))
            if find_subtree(cost_tree, to_search_1, i):
                cost_min = cost
                continue
            if to_search_2 and find_subtree(cost_tree, to_search_2, i):
                cost_min = cost
                continue

        return -1 if cost_min == (total_tree_cost+1) else cost_min

    def minimal_balanced_cost(self):
        '''choose variant'''
        return self.minimal_balanced_cost_correct()


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

        tree = Tree(edges, costs)
        cost = tree.minimal_balanced_cost()
        output_func(str(cost))


def parse_big_test(file_to_test=0):
    '''
        parse some big file HackerRank input
    '''
    class PrettyFileWriter:
        '''
            "A Gentle Introduction to Context Managers:
                The Pythonic Way of Managing Resources"
            https://alysivji.github.io/managing-resources-with-context-managers-pythonic.html
            "subclassing file objects"
            https://stackoverflow.com/questions/16085292
        '''
        def __init__(self, fileName):
            self.file = open(fileName, 'w')  # 'wb' for binary
            # PrettyFileWriter.set_crlf(False)

        def __enter__(self):
            # return self.file
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.file.close()
            # PrettyFileWriter.set_crlf(True)

        @staticmethod
        def set_crlf(text):
            '''force LF to have exactly same output

                https://stackoverflow.com/questions/25551634/only-do-lf-line-feed-at-the-end-of-print-in-python
            '''
            # pylint: disable=multiple-imports
            import msvcrt, os, sys  # noqa: E401
            msvcrt.setmode(sys.stdout.fileno(),
                           os.O_TEXT if text else os.O_BINARY)

        def writenl(self, line):
            '''
                normal "write" function, but also add a new line
                    (the reason of this "subclassing", PrettyFileWriter)
            '''
            # self.file.write(line.encode('utf8'))
            # self.file.write('\n'.encode('utf8'))
            self.file.write(line)
            self.file.write('\n')

    if file_to_test in [0, 1]:
        fptr = open('input01.txt', 'r')  # -1 10 13 5 297
        parse_with(fptr.readline, print)
    if file_to_test in [0, 2]:
        fptr = open('input03.txt', 'r')  # 1714 5016 759000000000 -1 6
        parse_with(fptr.readline, print)
        if 0:  # pylint: disable=using-constant-test
            with PrettyFileWriter('output03-mine.txt') as fptr_w:
                parse_with(fptr.readline, fptr_w.writenl)
    if file_to_test in [4]:
        fptr = open('input04.txt', 'r')  # ... big
        parse_with(fptr.readline, print)


def tests():
    '''
        tests for the current problem

        pass -O to ignore assertions and gain some time:
            py -3 -O ./prob.py
    '''
    sample_trees =\
        [Tree([[1, 2], [1, 3], [1, 4], [4, 5]], [15, 12, 8, 14, 13]),

         Tree([[1, 2], [1, 4], [2, 3], [1, 8], [8, 7], [7, 6], [5, 7]],
              [1, 1, 1, 18, 10, 11, 5, 6]),
         Tree([[1, 2], [1, 4], [2, 3], [1, 8], [8, 7], [7, 6], [5, 6]],
              [1, 1, 1, 18, 10, 11, 5, 6]),

         Tree([[1, 3], [3, 5], [1, 2], [2, 4], [6, 4]],
              [100, 100, 99, 99, 98, 98]),
         Tree([[1, 3], [3, 5], [1, 2], [2, 4], [6, 4]],
              [4, 4, 3, 3, 2, 2]),
         Tree([[1, 2], [1, 4], [2, 3], [4, 5], [6, 5]],
              [3, 2, 1, 3, 2, 1]),
         # a "complete" version of the previous
         Tree([[1, 2], [1, 4], [2, 3], [4, 5], [6, 5], [4, 7]],
              [3, 2, 1, 3, 2, 1, 6]),

         Tree([[1, 2], [1, 3], [3, 5], [4, 1]], [1, 2, 2, 1, 1]),
         ]
    missed_trees =\
        [Tree([[1, 2], [1, 3], [1, 4], [2, 5], [4, 6]],
              [12, 10, 8, 12, 14, 12]),
         # it finds value between the removed children
         Tree([[1, 2], [3, 1], [2, 4], [2, 5], [2, 6]],
              [7, 7, 4, 1, 1, 1]),
         ]
    no_solution_trees =\
        [Tree([[1, 2], [1, 3]], [1, 3, 5]),
         Tree([], [1]),
         ]

    def test_print(trees_list):
        for i in trees_list:
            for j in i:
                print(j)

    if 0:  # pylint: disable=using-constant-test
        test_print([sample_trees, missed_trees, no_solution_trees, ])

    assert sample_trees[0].minimal_balanced_cost() == 19
    assert sample_trees[1].minimal_balanced_cost() == 10
    assert sample_trees[2].minimal_balanced_cost() == 10
    assert sample_trees[3].minimal_balanced_cost() == 297
    assert sample_trees[4].minimal_balanced_cost() == 9
    assert sample_trees[5].minimal_balanced_cost() == 6
    assert sample_trees[6].minimal_balanced_cost() == 0
    assert sample_trees[7].minimal_balanced_cost() == 2
    assert missed_trees[0].minimal_balanced_cost() == 4
    assert missed_trees[1].minimal_balanced_cost() == -1
    assert no_solution_trees[0].minimal_balanced_cost() == -1
    assert no_solution_trees[1].minimal_balanced_cost() == -1

    if 1:  # pylint: disable=using-constant-test
        tree = missed_trees[1]
        print(tree)
        result = tree.minimal_balanced_cost()
        print(result)


def main():
    '''main'''
    tests()
    # parse_big_test()


if __name__ == "__main__":
    main()
