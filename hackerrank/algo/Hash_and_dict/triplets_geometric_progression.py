#!/usr/bin/env python3
# coding=utf-8
'''
    Calculate the number of triplets in geometric progression.
    https://www.hackerrank.com/challenges/count-triplets-1/problem

    Fantastic problem with an easy enough solution (... when spotted):
    - calculate after each change in sorting
    - keep track of the distribution:
        - single values
        - couples (val, val* ratio) waiting to be completed
    1 is a special case: only the single values distribution counts

    tag_combinatorics (alternate: tag_combinations)
'''


def combinations_3(number):
    '''calculate combinations of three'''
    assert number >= 2
    return number*(number-1)*(number-2)//6


def combinations_2(number):
    '''calculate combinations of two'''
    assert number >= 1
    return number*(number-1)//2


def count_triplets_dic(dic, ratio, debug_val=0):
    '''
        calculate the number of triplets for the given dictionary

        dic of values with their count
    '''
    assert ratio != 1

    triplets_no = 0
    for i in dic:
        if i*ratio in dic and i*ratio*ratio in dic:
            triplets_no += (dic[i]*dic[i*ratio]*dic[i*ratio*ratio])

    if debug_val and triplets_no:
        print(debug_val, "count_triplets_dic: ", triplets_no)

    return triplets_no


def count_triplets_ratio_1(arr):
    '''
        calculate the number of triplets for the given array with ratio 1
    '''
    dic_values = {}
    for i in arr:
        if i in dic_values:
            dic_values[i] += 1
        else:
            dic_values[i] = 1

    triplets_no = 0
    for i in dic_values:
        if dic_values[i] > 2:
            triplets_no += combinations_3(dic_values[i])
    return triplets_no


def count_triplets_6(arr, ratio):
    '''
        the sixth version - keep two dictionaries:
        - previous single values
        - previous couples
    '''
    if ratio == 1:
        return count_triplets_ratio_1(arr)

    # print(arr)

    def count_triplets_between(dic_values, dic_couples, dic_next, ratio,
                               debug_val=0):
        assert ratio != 1

        triplets_no = 0

        for i in dic_next:
            if i % (ratio*ratio) == 0:
                if i//(ratio*ratio) in dic_couples:
                    triplets_no += dic_next[i]*dic_couples[i // (ratio*ratio)]
            if i % ratio == 0 and i*ratio in dic_next and\
               i//ratio in dic_values:
                add = dic_values[i//ratio]*dic_next[i]*dic_next[i*ratio]
                triplets_no += add

        if debug_val and triplets_no:
            print(debug_val, "count_triplets_between: ", triplets_no)

        return triplets_no

    def add_from(dic_values, dic_couples, dic_next, ratio):
        assert ratio != 1

        def add_couple(dic_couples, couple, val):
            assert val
            if couple in dic_couples:
                dic_couples[couple] += val
            else:
                dic_couples[couple] = val

        #   add couples
        for i in dic_next:
            if i % ratio == 0 and i//ratio in dic_values:
                val = dic_next[i]*dic_values[i//ratio]
                add_couple(dic_couples, i//ratio, val)
            if i*ratio in dic_next:
                add_couple(dic_couples, i, dic_next[i]*dic_next[i*ratio])

        #   add simple values
        for i in dic_next:
            if i in dic_values:
                dic_values[i] += dic_next[i]
            else:
                dic_values[i] = dic_next[i]

    # dic of values
    dic_values = {}
    # contains the first member of the couple:
    #   (val) stands for (val, val*ratio)
    dic_couples = {}

    triplets_no = 0
    curr = {}
    last = arr[0]
    for i in arr:
        if i < last:
            assert curr
            triplets_no += count_triplets_dic(curr, ratio)
            triplets_no += count_triplets_between(dic_values, dic_couples,
                                                  curr, ratio)

            add_from(dic_values, dic_couples, curr, ratio)
            curr = {}

        if i in curr:
            curr[i] += 1
        else:
            curr[i] = 1
        last = i

    if curr:
        triplets_no += count_triplets_dic(curr, ratio, 0)
        triplets_no += count_triplets_between(dic_values, dic_couples,
                                              curr, ratio, 0)

    return triplets_no


def count_triplets(arr, ratio):
    '''count triplets problem preview'''
    return count_triplets_6(arr, ratio)


def countTriplets(arr, ratio):
    '''count triplets problem preview : official function name'''
    return count_triplets(arr, ratio)


def count_triplets_tup(tup):
    '''count triplets problem preview, but with a touple as entry'''
    arr = tup[0]
    ratio = tup[1]
    print(len(arr), ratio)
    return countTriplets(arr, ratio)


def from_file(file_path):
    '''read (large) data entry from a file'''
    with open(file_path) as file:
        (size, ratio) = (int(i) for i in file.readline().strip().split())
        integers = [int(i) for i in file.readline().strip().split()]
    # print(size, ration, len(integers))
    assert size == len(integers)
    return (integers, ratio)


def test_1():
    '''ratio 1 missed test'''
    distribution = {1: 10095, 100: 9875, 10000: 10000, 100000: 9746,
                    1000000: 10004, 1000000000: 10140, 10000000: 9960,
                    100000000: 9935, 1000: 10238, 10: 10005}
    triplets_no = 0
    for i in distribution:
        triplets_no += combinations_3(distribution[i])
    print(triplets_no)


def test_1_file(file_path):
    '''ratio 1 missed test'''
    arr, ratio = from_file(file_path)
    assert ratio == 1

    distribution = {}
    for i in arr:
        if i in distribution:
            distribution[i] += 1
        else:
            distribution[i] = 1
    print(distribution)

    #   {1: 10095, 100: 9876, 10000: 10000, 100000: 9747,
    #    1000000: 10004, 1000000000: 10140, 10000000: 9960,
    #    100000000: 9935, 1000: 10238, 10: 10005}
    triplets_no = 0
    for i in distribution:
        triplets_no += combinations_3(distribution[i])
    print(triplets_no)


def tests_assertions():
    '''
        known small cases
    '''
    assert countTriplets([1, 4, 16, 64], 4) == 2
    assert countTriplets([1, 2, 2, 4], 2) == 2
    assert countTriplets([1, 3, 9, 9, 27, 81], 3) == 6
    assert countTriplets([1, 5, 5, 25, 125], 5) == 4

    assert countTriplets([1, 4, 5], 1) == 0
    assert countTriplets([1, 4, 4, 4], 1) == 1
    assert countTriplets([1, 4, 4, 4, 4], 1) == 4
    assert countTriplets([1]*100, 1) == 161700

    #  ... but gets often 4
    assert countTriplets([1, 2, 1, 2, 4], 2) == 3
    assert countTriplets([1, 2, 1, 2, 2, 4], 2) == 5

    assert countTriplets([1, 2, 1, 2, 2, 4, 1, 2, 4, 4], 2) == 21
    assert countTriplets([1, 2, 1, 2, 2, 4, 1, 2, 4, 2, 4], 2) == 24

    assert countTriplets([1, 2, 4, 1, 2, 4, 8], 2) == 7
    assert countTriplets([1, 2, 4, 8, 1, 2, 4, 8], 2) == 8

    # special 1 cases
    assert count_triplets([1, 2, 1, 2, 4], 1) == 0
    assert count_triplets([1, 2, 1, 2, 4, 1], 1) == 1
    assert count_triplets([1, 2, 4, 8, 1, 2, 4, 2, 4, 2, 8], 1) == 5
    assert count_triplets([1, 2, 4, 8, 1, 2, 4, 2, 4, 2, 8, 4, 8], 1) == 9


def tests_files():
    '''
        large arrays given as files
    '''
    #   100000: 2325652489
    result = count_triplets_tup(from_file("test_10000"))
    print(result)
    assert result == 2325652489

    #  1339347780085
    result = count_triplets_tup(from_file("test_10000_2"))
    print(result)
    assert result == 1339347780085

    #   100000 1:  1667018988625
    result = count_triplets_tup(from_file("input11.txt"))
    print(result)
    assert result == 1667018988625
    # test_1_file("input11.txt")
    # test_1()


def tests():
    '''
        tests for the current problem
    '''
    tests_assertions()
    tests_files()


if __name__ == '__main__':
    tests()
