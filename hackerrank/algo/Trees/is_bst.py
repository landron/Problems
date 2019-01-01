#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/ctci-is-binary-search-tree

    tag_tree, tag_binary_tree, tag_binary_sarch_tree
'''
# import sys
# import math


class Node:
    '''
        Node in a binary tree
    '''
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    @staticmethod
    def in_order_norec(node, result):
        '''store the indices of the in-order traversal
                not using recursivity

            https://en.wikipedia.org/wiki/Tree_traversal#In-order_(LNR)
        '''
        stack = []
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                result.append(node)  # visit
                node = node.right

    @staticmethod
    def in_order(node, result):
        '''store the indices of the in-order traversal'''
        return Node.in_order_norec(node, result)

    def __str__(self):
        traversal = []
        Node.in_order(self, traversal)

        result = ""
        for i in traversal:
            result += str(i.data)
            result += ' '
        return result


def check_binary_tree_rec(root, sup, inf):
    '''
        recursively check if the given binary tree is a binary search tree
    '''
    # pylint: disable=too-many-return-statements

    def get_sup(one, two):
        return max(one, two)

    def get_inf(one, two):
        if -1 == one:
            return two
        if -1 == two:
            return one
        return min(one, two)

    if root.left:
        # if (875 == root.data or 875 == root.left.data):
        #     print("left", root.data, root.left.data, inf)
        if root.data <= root.left.data:
            return False
        if inf >= 0 and root.left.data <= inf:
            return False
        if not check_binary_tree_rec(root.left, get_inf(sup, root.data), inf):
            return False

    if root.right:
        # if (875 == root.data or 875 == root.right.data):
        #     print("right", root.data, root.right.data, sup)
        if root.data >= root.right.data:
            return False
        if root.right.data >= sup >= 0:
            return False
        if not check_binary_tree_rec(root.right, sup, get_sup(inf, root.data)):
            return False

    return True


def check_binary_tree(root):
    '''
        check if the given binary tree is a binary search tree
    '''
    return check_binary_tree_rec(root, -1, -1)


def tree_from_list(nodes):
    '''
        construct a tree from a list of nodes (the hackerrank way)
    '''

    # height = round(math.log2(1+len(nodes)))
    # print(height)
    size = len(nodes)

    root = Node(nodes[(1+size)//2-1])
    # print("added", root.data)

    level_now = [root]
    level_next = []

    level = 2
    while level < size:
        period = (1+size)//(2*level)

        where = period
        for node in level_now:
            node.left = Node(nodes[where-1])
            where += (period*2)
            node.right = Node(nodes[where-1])
            where += (period*2)

            level_next.append(node.left)
            level_next.append(node.right)

            # print("added", node.left.data, node.right.data)

        level_now = level_next
        level_next = []
        level *= 2

    return root


def from_file(file_path):
    '''read (large) data entry from a file'''
    with open(file_path) as file:
        height = int(file.readline().strip())
        values = [int(i) for i in file.readline().strip().split()]
        if 0:  # pylint: disable=using-constant-test
            last = 0
            for i in values:
                if i != last+1:
                    print(i)
                last = i
        # print(len(values), 2 << height)
        assert len(values) == (2 << height) - 1

        tree = tree_from_list(values)
        print(tree)
        print(check_binary_tree(tree))


def tests():
    '''
        tests for the current problem
    '''
    assert check_binary_tree(tree_from_list([1, 2, 3, 4, 5, 6, 7]))
    assert not check_binary_tree(tree_from_list([1, 2, 4, 3, 5, 6, 7]))

    # from_file('input10.txt')


if __name__ == '__main__':
    tests()
