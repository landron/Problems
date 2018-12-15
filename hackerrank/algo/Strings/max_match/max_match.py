#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/common-child/problem
        This is a tough enough problem, not a medium one anyway

    tag_class , tag_string_match , tag_elapsed_time
    tag_dynamic_prog

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
        '''optimization needed'''
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


def find_max_match(str1, str2, debug=False):
    '''determine the maximum submatch string between the two'''

    if debug:
        print("find_max_match", str1, str2)
        print("start: ", datetime.datetime.now().time())
        print()

    rec_data = lambda: None  # noqa: E731 do not assign a lambda expression,
    #                                use a def
    rec_data.debug = debug
    rec_data.start = time.time()
    rec_data.best_match_len = 0
    rec_data.match_len = 0

    result = find_max_match_rec(str1, str2, rec_data)
    if debug:
        print("Elapsed time:", int(time.time() - rec_data.start), "sec.")
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
        assert find_max_match('abcd', 'cefb') == 'b'
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

    #   elapsed time: around 0.5s
    if 0:  # pylint: disable=using-constant-test
        result = find_max_match(
            'WEWOUCUIDGCGTRMEZEPXZFEJWISRSBBSYXAYDFEJJDLEBVHHKS',
            'FDAGCXGKCTKWNECHMRXZWMLRYUCOCZHJRRJBOAJOQJZZVUYXIC', True)
        print(result)
        assert len(result) == 15
        assert result in ['DGCGTRMZJRBAJJV', 'DGCGTMZZJRBAJJV',
                          'DGCGTRXZJRBAJJV']

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
        assert result == 'YLBRYFZYIVMWSZTKMVOQKYEEYSP'

    # result = find_max_match('abcd', 'abdc', True)
    # print(result, len(result))


if __name__ == "__main__":
    tests()
