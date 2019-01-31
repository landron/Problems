#!/usr/bin/env python3
# coding=utf-8
'''
    ## Problem

    https://en.wikipedia.org/wiki/Longest_common_subsequence_problem

    https://www.hackerrank.com/challenges/common-child/problem
        This is a tough enough problem, not a medium one anyway

    Later:
        find_some_max_match_lcs: not only the maximum length,
            but also a substring
        https://www.hackerrank.com/challenges/dynamic-programming-classics-the-longest-common-subsequence/problem

    ## tags

    tag_class , tag_string_match , tag_elapsed_time
    tag_optimization

    tag_lcs

    ## Tries history

    - backtracking
        optimization 1: is_max_possible
            50 chars strings: from 83s to 10s

            15/60 points : 9/15 tests in timeout
        optimization 2: is_max_possible reused
            cannot squeeze more from this solution

        optimization 3: keep the maximum size in SizedDict
            this is even slower : 127s vs 83s

    - new different try: dynamic programming (quick search alike)
        very, very fast BUT fails

        it works with split_string_without_pivot, but much slower

        various little optimizations failed:
        - avoid calculating dictionary every time
        - get the pivot in the larger string (even wrong result!)

    - lcs
        recursively: "RecursionError: maximum recursion depth exceeded
            while calling a Python object"
        table: still does not passes all the cases in Python 3
            Python 2, PyPy3

            memory can still be reduced: only two lines needed at
                any given time

            >py -3 ./prob.py
            Result 1417
            Elapsed time: 22 sec.

            >py -2 ./prob.py
            ('Result', 1417)
            ('Elapsed time:', 12, 'sec.')

            Python 3 : do not use max !!!
'''
# import datetime
import time


def find_max_match_lcs(str1, str2):
    '''determine the maximum submatch string between the two
        using "Longest common subsequence problem"
        https://en.wikipedia.org/wiki/Longest_common_subsequence_problem

        RecursionError: maximum recursion depth exceeded while calling
            a Python object

        But this gives timeout on certain samples (Python3):
            only two lines & columns necessary, not all this table

            it passes even Python 3 after replacing the function 'max'

        Can be implemented using the next function, find_some_max_match_lcs,
            which really finds a substring.
    '''
    len1 = len(str1)
    len2 = len(str2)

    line1 = [0 for _ in range(1+len1)]
    line2 = [0 for _ in range(1+len1)]

    for i in range(1, 1+len2):
        for j in range(1, 1+len1):
            if str1[j-1] == str2[i-1]:
                line2[j] = line1[j-1] + 1
            else:
                line2[j] = line2[j-1] if line2[j-1] > line1[j] else line1[j]
        line1, line2 = line2, line1

    # print(table)
    return line1[-1]


def find_some_max_match_lcs(list1, list2):
    '''
        find a maximum submatch string between the two
        (not only the length, but also a submatch string (a "sample")).

        A generalized version of the previous, find_max_match_lcs, more
            memory hungry.
    '''
    len1 = len(list1)
    len2 = len(list2)

    line1 = [[] for i in range(1+len1)]
    line2 = [[] for i in range(1+len1)]

    for i in range(1, 1+len2):
        for j in range(1, 1+len1):
            if list1[j-1] == list2[i-1]:
                line2[j] = line1[j-1] + [list1[j-1]]
            elif len(line2[j-1]) > len(line1[j]):
                line2[j] = line2[j-1]
            else:
                line2[j] = line1[j]
        line1, line2 = line2, line1
        # print(line1)

    # print(table)
    return line1[-1]


def max_match_lcs_str(str1, str2):
    '''find_some_max_match_lcs shortcut for strings'''
    return ''.join(find_some_max_match_lcs(str1, str2))


def large_test(filename):
    '''
        test that crashes python
    '''
    start = time.time()

    with open(filename) as file:
        content = file.readlines()
        str1 = content[0]
        str2 = content[1]

        result = find_max_match_lcs(str1, str2)
        print("Result", result)
        print("Elapsed time:", int(time.time() - start), "sec.")
        return result


def tests():
    '''
        tests for the current problem

        pass -O to ignore assertions and gain some time:
            py -3 -O ./prob.py
    '''
    # assert False

    if 1:  # pylint: disable=using-constant-test
        assert find_max_match_lcs('abc', 'def') == 0
        assert find_max_match_lcs('bac', 'fed') == 0
        assert find_max_match_lcs('abc', 'dcf') == 1
        assert find_max_match_lcs('abcd', 'befc') == 2
        assert find_max_match_lcs('abcd', 'cefb') == 1
        assert find_max_match_lcs('abcd', 'beca') == 2
        assert find_max_match_lcs('abcd', 'abec') == 3
        assert find_max_match_lcs('abcd', 'abdc') == 3

        assert find_max_match_lcs('AquaVitae', 'AruTaVae') == 6
        assert find_max_match_lcs('HARRY', 'SALLY') == 2
        assert find_max_match_lcs('AA', 'BB') == 0
        assert find_max_match_lcs('NAAF', 'ARAA') == 2
        assert find_max_match_lcs('ABCDEF', 'FBDAMN') == 2

        assert find_max_match_lcs('ANAAF', 'ARAA') == 3
        assert find_max_match_lcs('SHINCHAN', 'NOHARAAA') == 3

    if 1:  # pylint: disable=using-constant-test
        result = find_max_match_lcs(
            'WEWOUCUIDGCGTRMEZEPXZFEJWISRSBBSYXAYDFEJJDLEBVHHKS',
            'FDAGCXGKCTKWNECHMRXZWMLRYUCOCZHJRRJBOAJOQJZZVUYXIC')
        assert result == 15

    if 1:  # pylint: disable=using-constant-test
        result = find_max_match_lcs(
            'ELGGYJWKTDHLXJRBJLRYEJWVSUFZKYHOIKBGTVUTTOCGMLEXWDSXEBKRZTQU'
            'VCJNGKKRMUUBACVOEQKBFFYBUQEMYNENKYYGUZSP',
            'FRVIFOVJYQLVZMFBNRUTIYFBMFFFRZVBYINXLDDSVMPWSQGJZYTKMZIPEGMV'
            'OUQBKYEWEYVOLSHCMHPAZYTENRNONTJWDANAMFRX')
        assert result == 27

    if 0:  # pylint: disable=using-constant-test
        result = large_test("input04.txt")
        assert result == 321

        # Result 1417
        # Elapsed time: 28 sec.
        #
        # Python 2:
        # 'Result', 1417)
        # 'Elapsed time:', 16, 'sec.')
        #
        # Final:
        #
        # Result 1417
        # Elapsed time: 17 sec.
        result = large_test("input05.txt")
        assert result == 1417

    if 1:  # pylint: disable=using-constant-test
        assert find_some_max_match_lcs([1, 2, 3, 4, 1], [3, 4, 1, 2, 1, 3])\
                == [3, 4, 1]  # attention: multiple solutions
        assert max_match_lcs_str('ANAAF', 'ARAA') == 'AAA'
        assert max_match_lcs_str('SHINCHAN', 'NOHARAAA') == 'NHA'


if __name__ == "__main__":
    tests()
