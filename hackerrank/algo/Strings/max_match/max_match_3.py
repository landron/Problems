#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/common-child/problem
        This is a tough enough problem, not a medium one anyway

    tag_class , tag_string_match , tag_elapsed_time
    tag_dynamic_prog

    tag_lcs
    https://en.wikipedia.org/wiki/Longest_common_subsequence_problem

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
import datetime
import time


class DictLetters():
    '''
        string and array of letters with their positions
    '''
    def __init__(self, string=''):
        # lowercase and uppercase ASCII
        self.dic = [[] for i in range(128)]
        self.str = string

        for i, val in enumerate(string):
            self.dic[ord(val)] += [i]

    def __str__(self):
        # result = str(self.count) + ': '
        result = ''
        result += self.presentation()
        return result

    def presentation(self):
        '''get a nice represenation of this dictionary'''
        result = ''
        for i, val in enumerate(self.dic):
            result += chr(i)*len(val)
        return result

    def contains(self, ch_next):
        '''does the string contains the character ?'''
        return self.dic[ord(ch_next)]

    def get_all(self, ch_next):
        '''get the list of positions of this character'''
        assert self.contains(ch_next)
        return self.dic[ord(ch_next)]

    def get(self, ch_next, first_or_last):
        '''get (one of) the position(s) in the string'''
        positions = self.get_all(ch_next)
        assert positions
        return positions[0] if first_or_last else positions[-1]


class DictCommon():
    '''
        dictionary of common letters
    '''
    def __init__(self, str1, str2):
        # lowercase and uppercase ASCII
        self.dic = [0] * 128

        self.count = 0
        for i in range(128):
            if str1.dic[i] and str2.dic[i]:
                self.dic[i] = min(len(str1.dic[i]), len(str2.dic[i]))
                self.count += self.dic[i]

    def __str__(self):
        result = ''
        for i, val in enumerate(self.dic):
            result += chr(i)*val
        return result

    def __len__(self):
        return self.count

    def contains(self, ch_next):
        '''does the string contains the character ?'''
        return self.dic[ord(ch_next)]

    def reduce(self, str_in):
        '''eliminate characters not in the common'''
        str_out = ''
        for i in str_in:
            if self.contains(i):
                str_out += i
        return DictLetters(str_out)


def find_max_match_rec(str1, str2, rec):
    '''
        find the best match recursively
            dynamic programming

        adding a find_max_match_rec_dict worsen the performance:
            93 -> 127
            (even if I tried to avoid too many recursivity levels)
    '''
    dict1 = DictLetters(str1)
    dict2 = DictLetters(str2)
    common = DictCommon(dict1, dict2)
    if len(common) <= 1:
        return str(common)
    if rec.match_len:
        if rec.match_len + len(common) <= rec.best_match_len:
            # print("Optimization:", len(common), rec.best_match_len)
            return ''

    dict1 = common.reduce(dict1.str)
    dict2 = common.reduce(dict2.str)

    if len(dict1.str) > len(dict2.str):
        dict1, dict2 = dict2, dict1

    assert len(dict1.str) >= 2  # already compared for common
    if len(dict1.str) == 2:
        pos1 = dict2.get(dict1.str[0], True)
        pos2 = dict2.get(dict1.str[1], False)
        assert pos1 != pos2
        return dict1.str if pos1 < pos2 else dict1.str[0]

    # go recursive

    def get_max(str_max, candidate):
        if len(candidate) > len(str_max):
            return candidate
        return str_max

    def split_string_keep_pivot(pivot):
        '''this one is very fast'''
        s1l = dict1.str[:pivot]
        s1r = dict1.str[pivot+1:]

        best_match = ''

        # positions of pivot in s2
        str2_list = dict2.get_all(dict1.str[pivot])
        for i in str2_list:
            left = find_max_match_rec(s1l, dict2.str[:i], rec)
            # rec.match_len += (1 + len(left))
            right = find_max_match_rec(s1r, dict2.str[i+1:], rec)
            # rec.match_len -= (1 + len(left))
            match = left+dict1.str[pivot]+right
            best_match = get_max(best_match, match)

        return best_match

    def split_string_without_pivot(pivot):
        '''optimization needed

            eliminating the pivot in the second string (like the pivot
            variant) is even much slower
        '''
        first = dict1.str[:pivot-1] + dict1.str[pivot+1:]
        return find_max_match_rec(first, dict2.str, rec)

    #   choose pivot

    def with_or_without_pivot():
        pivot = len(dict1.str) // 2
        # pivot = len(dict2.str) // 2

        best_match = split_string_keep_pivot(pivot)
        if rec.best_match_len < len(best_match):
            rec.best_match_len = len(best_match)
        match = split_string_without_pivot(pivot)
        return get_max(best_match, match)

    def all_pivots():  # pylint: disable=unused-variable
        '''much too slow'''
        best_match = ''
        for pivot, _ in enumerate(dict1.str):
            match = split_string_keep_pivot(pivot)
            best_match = get_max(best_match, match)
        return best_match

    return with_or_without_pivot()


def find_max_match_dp(str1, str2, debug):
    '''determine the maximum submatch string between the two
        using dynamic programming with a pivot
    '''

    rec_data = lambda: None  # noqa: E731 do not assign a lambda expression,
    #                                use a def
    rec_data.debug = debug
    rec_data.start = time.time()
    rec_data.best_match_len = 0
    rec_data.match_len = 0

    return find_max_match_rec(str1, str2, rec_data)


def find_max_match_lcs_rec(str1, str2, rec):
    '''determine the maximum submatch string between the two
        using "Longest common subsequence problem"
        https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
    '''

    if not str1 or not str2:
        return ''
    if rec.table[len(str1)-1][len(str2)-1]:
        return rec.table[len(str1)-1][len(str2)-1]

    solution = ''
    if str1[-1] == str2[-1]:
        solution = find_max_match_lcs_rec(str1[:-1], str2[:-1], rec) + str1[-1]
    else:
        first = find_max_match_lcs_rec(str1[:-1], str2, rec)
        second = find_max_match_lcs_rec(str1, str2[:-1], rec)
        solution = first if len(first) > len(second) else second
    rec.table[len(str1)-1][len(str2)-1] = solution
    return solution


def find_max_match_lcs_no_rec_1(str1, str2, rec):
    '''determine the maximum submatch string between the two
        using "Longest common subsequence problem"
        https://en.wikipedia.org/wiki/Longest_common_subsequence_problem

        RecursionError: maximum recursion depth exceeded while calling
            a Python object

        But this gives timeout on certain samples
    '''
    table = rec.table
    len1 = len(str1)
    len2 = len(str2)

    for i in range(len1):
        table[i][0] = 0
    for i in range(len2):
        table[0][i] = 0

    for i in range(1, 1+len1):
        # print(i)
        for j in range(1, 1+len2):
            if str1[i-1] == str2[j-1]:
                table[i][j] = table[i-1][j-1] + 1
            else:
                table[i][j] = max(table[i][j-1], table[i-1][j])
    # print(table)
    return table[len1][len2]


def find_max_match_lcs_no_rec(str1, str2):
    '''determine the maximum submatch string between the two
        using "Longest common subsequence problem"
        https://en.wikipedia.org/wiki/Longest_common_subsequence_problem

        RecursionError: maximum recursion depth exceeded while calling
            a Python object

        But this gives timeout on certain samples (Python3):
            only two lines & columns necessary, not all this table

            it passes even Python 3 after replacing the function 'max'
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


def find_max_match_lcs_rec_only_len(str1, str2, rec):
    '''determine the maximum submatch string between the two
        using "Longest common subsequence problem"
        https://en.wikipedia.org/wiki/Longest_common_subsequence_problem

        RecursionError: maximum recursion depth exceeded while calling
            a Python object
    '''

    if not str1 or not str2:
        return 0
    if -1 != rec.table[len(str1)-1][len(str2)-1]:
        return rec.table[len(str1)-1][len(str2)-1]

    solution = 0
    if str1[-1] == str2[-1]:
        eq_len = 1
        while len(str1) >= eq_len+1 and len(str2) >= eq_len+1\
            and str1[-(eq_len+1)] == str2[-(eq_len+1)]:
            eq_len += 1

        solution = find_max_match_lcs_rec_only_len(
            str1[:-eq_len], str2[:-eq_len], rec) + eq_len
    else:
        first = find_max_match_lcs_rec_only_len(str1[:-1], str2, rec)
        second = find_max_match_lcs_rec_only_len(str1, str2[:-1], rec)
        solution = first if first > second else second

    # rec.calculated += 1
    # print(rec.calculated)

    rec.table[len(str1)-1][len(str2)-1] = solution
    return solution


def find_max_match_lcs(str1, str2, debug, only_len=False):
    '''determine the maximum submatch string between the two
        using "Longest common subsequence problem"
        https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
    '''
    rec = lambda: None  # noqa: E731 do not assign a lambda expression,
    #                                use a def
    rec.debug = debug
    # rec.calculated = 0

    len1 = len(str1)
    len2 = len(str2)

    if not only_len:
        rec.table = [[None for _ in range(1+len2)]
                     for _ in range(1+len1)]
        return find_max_match_lcs_rec(str1, str2, rec)

    # rec.table = [[-1 for _ in range(1+len2)]
    #              for _ in range(1+len1)]
    # # return find_max_match_lcs_rec_only_len(str1, str2, rec)
    # return find_max_match_lcs_no_rec(str1, str2, rec)
    return find_max_match_lcs_no_rec(str1, str2)


def find_max_match(str1, str2, debug=False):
    '''determine the maximum submatch string between the two'''

    start = time.time()
    if debug:
        print("find_max_match", str1, str2)
        print("start: ", datetime.datetime.now().time())
        print()

    # result = find_max_match_dp(str1, str2, debug)
    result = find_max_match_lcs(str1, str2, debug)
    if debug:
        print("Elapsed time:", int(time.time() - start), "sec.")
    return result


def large_test():
    '''
        test that crashes python
    '''
    start = time.time()

    # filename = "input04.txt"

    # Result 1417
    # Elapsed time: 28 sec.
    #
    # Python 2:
    # 'Result', 1417)
    # 'Elapsed time:', 16, 'sec.')
    filename = "input05.txt"

    with open(filename) as file:
        content = file.readlines()
        str1 = content[0]
        str2 = content[1]

        # print(len(str1), len(str2))

        result = find_max_match_lcs(str1, str2, True, True)
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
        assert find_max_match('abc', 'def') == ''
        assert find_max_match('bac', 'fed') == ''
        assert find_max_match('abc', 'dcf') == 'c'
        assert find_max_match('abcd', 'befc') == 'bc'
        assert find_max_match('abcd', 'cefb') in ['b', 'c']
        assert find_max_match('abcd', 'beca') == 'bc'
        assert find_max_match('abcd', 'abec') == 'abc'
        assert find_max_match('abcd', 'abdc') in ['abc', 'abd']

        assert find_max_match('AquaVitae', 'AruTaVae') == 'AuaVae'
        assert find_max_match('HARRY', 'SALLY') == 'AY'
        assert find_max_match('AA', 'BB') == ''
        assert find_max_match('NAAF', 'ARAA') == 'AA'
        assert find_max_match('ABCDEF', 'FBDAMN') == 'BD'

        # problems

        # crash
        assert find_max_match('ANAAF', 'ARAA') == 'AAA'
        # first partial solution is 'HA'
        assert find_max_match('SHINCHAN', 'NOHARAAA') == 'NHA'

        assert find_max_match_lcs(
            'WEWOUCUIDGCGTRMEZEPXZFEJWISRSBBSYXAYDFEJJDLEBVHHKS',
            'FDAGCXGKCTKWNECHMRXZWMLRYUCOCZHJRRJBOAJOQJZZVUYXIC',
            False, True) == 15

    #   elapsed time: around 0.5s
    if 1:  # pylint: disable=using-constant-test
        result = find_max_match(
            'WEWOUCUIDGCGTRMEZEPXZFEJWISRSBBSYXAYDFEJJDLEBVHHKS',
            'FDAGCXGKCTKWNECHMRXZWMLRYUCOCZHJRRJBOAJOQJZZVUYXIC', True)
        print(result)
        assert len(result) == 15
        assert result in ['DGCGTRMZJRBAJJV', 'DGCGTMZZJRBAJJV',
                          'DGCGTRXZJRBAJJV', 'DGCGTEXZWRYJJBV']

    # should be 27 : YLBRYFZYIVMWSZTKMVOQKYEEYSP 27
    #   (and not YLBRUIBVXDSQJKMVOQBYEEYSP 25: when only the fast "with pivot"
    #   variant is used)
    #
    #   Elapsed time: 92 sec.
    #   YLBRYFZYIVMWSZTKMVOQKYEEYSP 27
    #
    #   new function added to avoid dictionaries creation
    #       Elapsed time: 129 sec.
    #       YLBRYFZYIVMWSZTKMVOQKYEEYSP 27
    if 1:  # pylint: disable=using-constant-test
        result = find_max_match(
            'ELGGYJWKTDHLXJRBJLRYEJWVSUFZKYHOIKBGTVUTTOCGMLEXWDSXEBKRZTQU'
            'VCJNGKKRMUUBACVOEQKBFFYBUQEMYNENKYYGUZSP',
            'FRVIFOVJYQLVZMFBNRUTIYFBMFFFRZVBYINXLDDSVMPWSQGJZYTKMZIPEGMV'
            'OUQBKYEWEYVOLSHCMHPAZYTENRNONTJWDANAMFRX', True)
        print(result, len(result))
        assert len(result) == 27
        assert result in ['YLBRYFZYIVMWSZTKMVOQKYEEYSP',
                          'RJYVUFZYIVMWSQGKMVOQBYEEYSP']

    # result = find_max_match_lcs('SHINCHAN', 'NOHARAAA', True, True)
    # print(result)
    # large_test()


if __name__ == "__main__":
    tests()
