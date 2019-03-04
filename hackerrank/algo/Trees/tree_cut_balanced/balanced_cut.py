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

    tag_hard

    flake8, pylint
'''


class TreeNode:
    '''
        a node in tree
    '''
    def __init__(self, node_id, parent, cost=0):
        self.nid = node_id
        self.parent = parent
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
                description += str(i.id)
                description += ', '
            description = description[:-2]
            description += ")"
            return description

        description = "("
        if not self.parent:
            description += "root (1)"
            assert self.nid == 1, "only for test"
        else:
            if with_parent:
                description += str(self.parent.nid)
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
        assert self == node.parent
        if self.adj_list:
            self.adj_list.append(node)
        else:
            self.adj_list = [node]


class Tree:
    '''
        a tree
    '''
    def __init__(self, edges, cost):
        nodes_no = len(cost)
        assert nodes_no == len(edges) + 1

        self.root = TreeNode(1, None, cost[0])
        self.cost_tree = []

        adj_list = Tree.make_adjacency_list(edges)

        queue = [self.root]
        while queue:
            node = queue.pop()
            assert adj_list[node.nid-1]
            for i in adj_list[node.nid-1]:
                child = TreeNode(i, node, cost[i-1])
                node.add_child(child)
                if adj_list[i-1]:
                    queue.append(child)

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
            adj[i] = list(adj[i])

        return adj


def tests():
    '''
        tests for the current problem

        pass -O to ignore assertions and gain some time:
            py -3 -O ./prob.py
    '''
    def test_print():
        trees = [Tree([[1, 2], [1, 3], [1, 4], [4, 5]], [15, 12, 8, 14, 13]),
                 Tree([[1, 2], [1, 4], [2, 3], [1, 8], [8, 7], [7, 6], [5, 7]],
                      [1, 1, 1, 18, 10, 11, 5, 6])]
        for i in trees:
            print(i)

    test_print()


def main():
    '''main'''
    tests()


if __name__ == "__main__":
    main()
