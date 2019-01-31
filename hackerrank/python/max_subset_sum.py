#!/bin/python3
'''
    https://www.hackerrank.com/challenges/max-array-sum/problem

    tag_dynamic

    I used some "inspiration" from the Discussions: see tag_warn for
    the tests that did not work. Unfortunately, the provided tests were
    too heavy to detect the cause of failure.
'''
# import os


def max_subset_sum_rec(arr):
    '''
        RecursionError: maximum recursion depth exceeded in comparison
    '''
    if not arr:
        return 0
    first = arr[0] if arr[0] > 0 else 0
    if len(arr) == 1:
        return first
    sum_without = max_subset_sum_rec(arr[1:])
    if not first:
        return sum_without
    sum_with = first + max_subset_sum_rec(arr[2:])
    return sum_with if sum_with > sum_without else sum_without


def max_subset_sum(arr):
    '''
        No recursion.

        max function can be slow.
    '''
    sum1 = sum2 = 0
    last1 = last2 = 0
    first = True
    for _, val in enumerate(arr):
        # negative numbers are not considered => they reset the two sums
        if val <= 0:
            sum_max = sum1 if sum1 > sum2 else sum2
            sum1 = sum2 = sum_max
            first = True
        else:
            # choose the (last) other one if more appropiate, there is
            #   already a value in between (just added to the other sum)
            if first:
                last1 = sum1
                if sum1 < last2:
                    sum1 = last2
                sum1 += val
            else:
                last2 = sum2
                if sum2 < last1:
                    sum2 = last1
                sum2 += val
            first = not first

    sum_max = sum1 if sum1 > sum2 else sum2
    return sum_max if sum_max > 0 else 0


def maxSubsetSum(arr):  # pylint: disable=invalid-name
    '''
        # Complete the maxSubsetSum function below.
    '''
    assert arr
    if len(arr) == 1:
        return arr[0]
    # sum_max = max_subset_sum_rec(arr)
    sum_max = max_subset_sum(arr)
    assert sum_max >= 0
    if not sum_max:
        arr.sort()
        sum_max = arr[-1]
    return sum_max


def parse_input():
    '''
        parse input in the HackerRank format
    '''
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    src = open('input00.txt', 'r')
    input_func = src.readline  # vs input

    _ = int(input_func())
    arr = list(map(int, input_func().rstrip().split()))

    res = maxSubsetSum(arr)

    # fptr.write(str(res) + '\n')
    # fptr.close()
    print(res)


def tests():
    '''
        unit tests, assertions
    '''
    assert maxSubsetSum([-2, 1, 3, -4, 5]) == 8
    assert maxSubsetSum([3, 7, 4, 6, 5]) == 13
    assert maxSubsetSum([2, 1, 5, 8, 4]) == 11

    assert maxSubsetSum([2, 1, 5, 8, 4, 3]) != 12  # ! tag_warn
    assert maxSubsetSum([2, 1, 5, 8, 4, 3]) == 13
    assert maxSubsetSum([2, 1, 5, 8, 7, 3]) == 14
    assert maxSubsetSum([2, 1, 5, 8, 4, 3, 0, 1]) == 14
    assert maxSubsetSum([2, 1, 5, 8, 4, 3, 5, 1]) == 16
    assert maxSubsetSum([2, 1, 5, 8, 4, 3, 1, 5]) == 18

    assert maxSubsetSum([1, 4, 2, 1, 3]) != 6  # ! tag_warn
    assert maxSubsetSum([1, 4, 2, 1, 3]) == 7

    assert maxSubsetSum([3, 5, -7, 8, 10]) == 15
    assert maxSubsetSum([3, 5, -7, 8, 10, -6, -6]) == 15
    assert maxSubsetSum([3, 5, -7, 8, 10, -6, -6, 2]) == 17
    assert maxSubsetSum([3, 5, -7, 8, 10, -6, -6, 2, 1]) == 17
    assert maxSubsetSum([3, 5, -7, 8, 10, -6, -6, 2, 2]) == 17
    assert maxSubsetSum([3, 5, -7, 8, 10, -6, -6, 2, 3]) == 18
    assert maxSubsetSum([-1, -2, -7, 8, 10]) == 10

    assert maxSubsetSum([3, 5, 3]) == 6
    assert maxSubsetSum([3, 5, 3, -1, 7, -2]) == 13
    assert maxSubsetSum([3, 5, 3, -1, 7, 6]) == 13
    assert maxSubsetSum([3, 5, 3, -1, 7, 8]) == 14
    assert maxSubsetSum([3, 5, 3, -1, 7, -1, 2, 3]) == 16

    assert maxSubsetSum([1, 0, 2]) == 3
    assert maxSubsetSum([1, 0, 2, 0]) == 3
    assert maxSubsetSum([1, 0, 2, 2, 1]) == 4
    assert maxSubsetSum([1, 0, 2, 0, 2, 1]) == 5

    assert maxSubsetSum([-1, -2, -7, -3]) == -1
    assert maxSubsetSum([-1, -2, 0, -7, -3]) == 0
    assert maxSubsetSum([-1, -2, 1, 0, -7, -3, 1]) == 2

    # res = maxSubsetSum([3, 5, -7, 8, 10, -6, -6, 2, 1])
    # print(res)


def main():
    '''main'''
    tests()
    # parse_input()


if __name__ == '__main__':
    main()
