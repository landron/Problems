#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/swap-nodes-algo/problem

    Source for binary tree:
        https://www.hackerrank.com/challenges/binary-search-tree-lowest-common-ancestor/problem

    \todo
        "RecursionError: maximum recursion depth exceeded in comparison"
        solution 1:   sys.setrecursionlimit(1500)
        solution 2:   traverse the binary tree without recursion

    tag_tree, tag_tree_binary
    tag_recursion, tag_no_recursion
    tag_class
'''
# import sys # setrecursionlimit


class Node():
    '''
        Node in a binary tree
    '''
    def __init__(self, info):
        self.info = info
        self.left = None
        self.right = None
        self.level = None

    def __str__(self):
        return str(self.info)

    @staticmethod
    def find_rec(node, val):
        '''find a node in the subtree starting recursively with this node'''
        assert node

        if node.info == val:
            return node
        found = Node.find(node.left, val) if node.left else None
        if found:
            return found
        found = Node.find(node.right, val) if node.right else None
        return found

    @staticmethod
    def find_no_rec(node, val):
        '''find a node in this subtree, not using recursivity'''
        assert node

        if node.info == val:
            return node

        stack = []
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                if node.info == val:
                    return node
                node = node.right

        return None

    @staticmethod
    def find(node, val):
        '''find a node in this subtree, not using recursivity'''
        assert node
        return Node.find_no_rec(node, val)

    def swap(self):
        '''swap the children of this node'''
        self.left, self.right = self.right, self.left

    @staticmethod
    def in_order_rec(node, result):
        '''store the indices of the in-order traversal
                using recursivity
        '''
        assert node

        if node.left:
            Node.in_order(node.left, result)
        result.append(node)
        if node.right:
            Node.in_order(node.right, result)

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


class BinaryTree():
    '''
        A binary tree
    '''
    def __init__(self, val=None):
        self.root = Node(val) if val else None

    def __str__(self):
        if not self.root:
            return ""
        traversal = self.in_order()
        result = ""
        for i in traversal:
            result += str(i.info)
            result += ' '
        return result

    def in_order(self, values=False):
        '''in-order traversal. returns nodes or values'''
        assert self.root

        result = []
        Node.in_order(self.root, result)

        if not values:
            return result
        result_val = [str(i.info) for i in result]
        return result_val

    def find(self, val):
        '''find a node in this tree'''
        assert self.root
        return Node.find(self.root, val)

    def add(self, val, left, right):
        '''add a new value to our tree'''

        node = None
        if not self.root:
            assert val == 1
            self.root = Node(val)
            node = self.root
        else:
            node = self.find(val)
        assert node

        assert not node.left
        if left != -1:
            node.left = Node(left)

        assert not node.right
        if right != -1:
            node.right = Node(right)

    @staticmethod
    def swap_for_rec(node, level, k):
        '''recursively swap for levels multiple of k'''
        assert node

        if level % k == 0:
            node.swap()
        if node.left:
            BinaryTree.swap_for_rec(node.left, level+1, k)
        if node.right:
            BinaryTree.swap_for_rec(node.right, level+1, k)

    @staticmethod
    def swap_no_rec(node, level, k):
        '''swap nodes for levels multiple of k'''
        assert node

        stack = []
        while stack or node:
            if node:
                if level % k == 0:
                    node.swap()

                if node.left:
                    stack.append((node.left, level+1))
                if node.right:
                    stack.append((node.right, level+1))
                node = None
            else:
                node, level = stack.pop()

    def swap_for_levels_multiple_of(self, k):
        '''swap child nodes for multiples of the given value'''
        assert k > 0

        # BinaryTree.swap_for_rec(self.root, 1, k)
        BinaryTree.swap_no_rec(self.root, 1, k)


def swapNodes(indexes, queries):
    '''hackerrank input to test the solution'''
    tree = BinaryTree(1)
    for val, i in enumerate(indexes):
        tree.add(val+1, i[0], i[1])

    result = []
    for i in queries:
        tree.swap_for_levels_multiple_of(i)
        result.append(tree.in_order(values=True))
    return result


def from_file(file_path):
    '''read (large) data entry from a file'''
    indexes = []
    queries = []
    with open(file_path) as file:
        size_input = int(file.readline().strip())
        for _ in range(size_input):
            left, right = (int(i) for i in file.readline().strip().split())
            indexes.append([left, right])
        size_queries = int(file.readline().strip())
        for _ in range(size_queries):
            queries.append(int(file.readline().strip()))

    # print(len(indexes)/2)  # 512

    # File "./prob4.py", line 173, in swap_for_rec
    # if level % k == 0:
    #     RecursionError: maximum recursion depth exceeded in comparison
    swapNodes(indexes, queries)


def tests():
    '''
        tests for the current problem
    '''
    test1 = BinaryTree()
    test1.add(1, 2, 3)
    print(test1)
    test1.swap_for_levels_multiple_of(1)
    print(test1)
    test1.swap_for_levels_multiple_of(1)
    print(test1)

    test2 = BinaryTree(1)
    for val, i in enumerate([(2, 3), (-1, 4), (-1, 5), (-1, -1), (-1, -1)]):
        test2.add(val+1, i[0], i[1])
    print(test2)
    test2.swap_for_levels_multiple_of(2)
    print(test2)

    swapNodes([[2, 3], [-1, -1], [-1, -1]], [1, 1])

    swapNodes([], [])
    swapNodes([], [1, 1])
    swapNodes([[2, 3]], [1, 2])


if __name__ == '__main__':
    # sys.setrecursionlimit(1500)

    tests()
    # from_file("input10.txt")
