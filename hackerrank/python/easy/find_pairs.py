#!/bin/python3
'''
    https://www.hackerrank.com/challenges/pairs/problem

    tag_search
'''
# import os


def get_pairs(k, arr):
    '''
        Purpose
            Find all the pairs that give the same given difference.

        Result
            The result contains only the bigger number.

        More
            A variant is to keep the "candidates" in a separate list,
            but here I prefer the two pointers technique
    '''
    result = []

    arr.sort()
    small = 0
    for i, val in enumerate(arr):
        while val - arr[small] >= k:
            if val - arr[small] == k:
                result.append(val)
            if small < i:
                small += 1
            else:
                break

    return result


def pairs(k, arr):
    '''
        Return the result in the HackerRank format.
    '''
    return len(get_pairs(k, arr))


def parse_input():
    '''
        parse input in the HackerRank format
    '''


def tests():
    '''
        unit tests, assertions
    '''
    assert pairs(1, [1, 2, 3, 4]) == [2, 3, 4]
    assert pairs(2, [1, 5, 3, 4, 2]) == [3, 4, 5]


def main():
    '''main'''
    tests()
    # parse_input()


if __name__ == '__main__':
    main()
