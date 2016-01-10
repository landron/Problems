
'''
    Problem
        Given a binary tree, find the root of the subtree with the maximum number of nodes which
         forms a binary search tree
    Solution:
        bottom-top: start from the leftest tree and try to enlarge the subtree
    TODO
        - new test cases
        - new representations
    Version 2016.01.10

    Representations:
    - complete: missing nodes are represented by 0
    - short: each subtree is a list (except for the leafs)

    >pylint --version
        No config file found, using default configuration
        pylint 1.5.2,
        astroid 1.4.3
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 9.90/10 (previous run: 9.32/10, +0.58)
'''

# sr = short representation
def print_tree_sr(tree_in):
    '''print the tree's content - short representation'''
    assert isinstance(tree_in, list) or isinstance(tree_in, int)
    if isinstance(tree_in, list):
        print(tree_in[0])
    else:   # leaf
        print(tree_in)
        return

    if len(tree_in) > 1:
        print_tree_sr(tree_in[1])
        if len(tree_in) > 2:
            print_tree_sr(tree_in[2])

# sr = short representation
def largest_bst_step_sr(tree_in, solution):
    '''find the largest subtree - short representation'''
    assert isinstance(tree_in, list)
    assert len(tree_in) > 1
    assert len(tree_in) < 4
    value = tree_in[0] if isinstance(tree_in, list) else tree_in

    good_children = True
    children_l = 0
    children_r = 0

    if len(tree_in) > 1:
        if isinstance(tree_in[1], list):
            children_l = largest_bst_step_sr(tree_in[1], solution)
            good_children = tree_in[1][0] < value and children_l != 0
        elif tree_in[1] >= value:
            good_children = False
        else:
            children_l = 1
        if len(tree_in) > 2:
            if isinstance(tree_in[2], list):
                children_r = largest_bst_step_sr(tree_in[2], solution)
                good_children = good_children and tree_in[2][0] > value and children_r != 0
            elif tree_in[2] < value:
                good_children = False
            else:
                children_r = 1

    if good_children:
        nodes = children_l + children_r + 1
        if nodes >= solution.best.nodes:
            solution.best.nodes = nodes
            solution.best.root = tree_in
        return nodes
    else:
        return 0

def print_tree(tree_in, index):
    '''print the tree's content - complete representation'''
    print(tree_in[index])
    if 2*index+1 < len(tree_in):
        if tree_in[2*index+1] != 0:
            print_tree(tree_in, 2*index+1)
        if 2*index+2 < len(tree_in) and tree_in[2*index+2] != 0:
            print_tree(tree_in, 2*index+2)

def largest_bst_step(tree_in, index, solution):
    '''find the largest subtree - complete representation'''
    good_children = True
    children_l = 0
    children_r = 0

    if 2*index+1 < len(tree_in):
        if tree_in[2*index+1] != 0:
            if tree_in[2*index+1] >= tree_in[index]:
                good_children = False
            children_l = largest_bst_step(tree_in, 2*index+1, solution)
        if 2*index+2 < len(tree_in) and tree_in[2*index+2] != 0:
            if tree_in[2*index+2] < tree_in[index]:
                good_children = False
            children_r = largest_bst_step(tree_in, 2*index+2, solution)

    if good_children:
        nodes = children_l + children_r + 1
        if nodes >= solution.best.nodes:
            solution.best.nodes = nodes
            solution.best.root = index
        return nodes
    else:
        return 0

# TODO:   detect short representation
def largest_bst(tree_in, short_representation=False, to_print=False):
    '''find the largest subtree: common entry function'''
    assert tree_in

    solution = lambda: 0
    solution.best = lambda: 0
    solution.best.nodes = 0
    solution.best.root = 0

    if short_representation:
        largest_bst_step_sr(tree_in, solution)
    else:
        largest_bst_step(tree_in, 0, solution)
    if to_print:
        if short_representation:
            print_tree_sr(solution.best.root)
        else:
            print_tree(tree_in, solution.best.root)
        print(solution.best.nodes, "nodes")

    return (solution.best.root, solution.best.nodes)

def debug_validations():
    """all the assertions"""
    assert largest_bst([3]) == (0, 1)
    assert largest_bst([3, 2, 1]) == (2, 1)
    assert largest_bst([1, 2, 3]) == (2, 1)
    assert largest_bst([2, 1, 3]) == (0, 3)
    assert largest_bst([3, 2, 4, 1]) == (0, 4)
    assert largest_bst([3, 2, 3, 1]) == (0, 4)
    assert largest_bst([8, 3, 0, 2, 4, 0, 0, 1]) == (0, 5)
    assert largest_bst([8, 3, 4, 2, 4, 0, 0, 1]) == (1, 4)
    # short representation
    assert largest_bst([9, [4, 5, [6, [4, 2, 6], [9, [4, [3, 2]], 11]]]], True)[1] == 9
    # the real test sample
    assert largest_bst([8, 3, 4, 2, 4, 9, 7, 1, 0, 0, 0, 8, 9]) == (1, 4)
    assert largest_bst([8, [3, [2, 1], 4], [4, [9, 8, 9], 7]], True) == ([3, [2, 1], 4], 4)

def bst_standard_test():
    '''some standard demonstration test'''
    the_tree = [8, [3, [2, 1], 4], [4, [9, 8, 9], 7]]
    largest = largest_bst(the_tree, True)
    print("Largest BST for")
    print(the_tree)
    print("is")
    print(largest[0], "("+str(largest[1]), "nodes)")

if __name__ == "__main__":
    debug_validations()

    bst_standard_test()
