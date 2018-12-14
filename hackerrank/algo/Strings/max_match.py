#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/common-child/problem
        This is a tough enough problem, not a medium one anyway

    tag_class , tag_string_match , tag_elapsed_time
    tag_optimization

    optimization 1: is_max_possible
        50 chars strings: from 83s to 10s

        15/60 points : 9/15 tests in timeout
    optimization 2: is_max_possible reused
        cannot squeeze more from this solution
'''
import datetime
import time


class StringRec():
    '''
        structure used for the recursivity match search:
            - str : immutable
    '''
    def __init__(self, string):
        assert string

        self.str = string
        self.pos = 0

        # lowercase and uppercase ASCII
        self.dic = 128 * [0]
        for i in self.str:
            self.dic[ord(i)] += 1

    def __str__(self):
        result = "("
        result += self.str[self.pos:]
        result += ", "
        for i, val in enumerate(self.dic):
            if val:
                result += chr(i)
                result += ':'
                result += str(val)
                result += ' '
        result = result[:-1]
        result += ")"
        return result

    def value(self):
        '''the current (next to process) value of the string'''
        return self.str[self.pos:]

    def length(self):
        '''the length of the value of the string'''
        return len(self.str)-self.pos

    def next(self):
        '''the next character to process'''
        return self.str[self.pos]

    def can_advance(self):
        '''have we reach the end of the string ?'''
        return self.pos < len(self.str)

    def advance(self):
        '''increment: advance to the next character'''
        assert self.can_advance()

        if self.contains(self.next()):
            self.__reduce_next()
        self.pos += 1

    def __reduce_next(self):
        ch_next = self.next()
        assert self.contains(ch_next), "{0} should contain '{1}'.".\
            format(self.str[self.pos], ch_next)
        self.dic[ord(ch_next)] -= 1

    def contains(self, ch_next):
        '''does the string contains the character ?'''
        return self.dic[ord(ch_next)] > 0

    def __seek(self, pos):
        assert pos < len(self.str)
        self.pos = pos

    def current(self):
        '''return the current mutable data'''
        return (self.pos, self.dic[:])

    def reset(self, data):
        '''reset mutable data to restart the search'''
        self.__seek(data[0])
        self.dic = data[1][:]

    def max_possible(self, other):
        '''best match between those two strings'''
        max_match = ''
        for i, val in enumerate(self.dic):
            if val and other.contains(chr(i)):
                for _ in range(min(val, other.dic[i])):
                    max_match += chr(i)
        return max_match


def max_match_rec(str1, str2, recursive):
    '''
        determine recursively the maximum submatch string between the
         two entries
    '''
    if recursive.debug and recursive.level == 0:
        print("max_match_rec_in", str1, str2)

    def update_match(str1, str2, match):
        assert str1.next() == str2.next()
        match += str1.next()
        str1.advance()
        str2.advance()

    def can_advance(str1, str2):
        return str1.can_advance() and str2.can_advance()

    def update_max_match(match, max_match):
        if len(match) > len(max_match):
            max_match[:] = match
            print("update_max_match", ''.join(max_match), len(max_match))

    # this tiny optimization: 83s -> 9s
    def is_max_possible(recursive, str1, str2):
        max_possible = len(str1.max_possible(str2)) if str2 else str1.length()
        result = len(recursive.max_match) < len(recursive.match) +\
            max_possible
        # if not result:
        #     print("Optimization: ", len(recursive.max_match),
        #           len(recursive.match), max_possible)
        return result

    while str1.next() == str2.next():
        update_match(str1, str2, recursive.match)
        assert recursive.match
        update_max_match(recursive.match, recursive.max_match)

        if not can_advance(str1, str2):
            return

    if not is_max_possible(recursive, str1, str2):
        return

    data2_saved = str2.current()
    # match is immutable inside the loop
    match_saved = recursive.match[:]

    while True:
        if recursive.debug and recursive.level == 0:
            print("max_match_rec_02", str1.value(),
                  int(time.time() - recursive.start))

        while str1.can_advance() and not str2.contains(str1.next()):
            str1.advance()
        # optimization 2: 8s -> 6s
        if not str1.can_advance() or \
           not is_max_possible(recursive, str1, None):
            break

        while str2.next() != str1.next():
            assert str2.can_advance(), "the second string should contain '{0}'.\
                ".format(str1.next())
            str2.advance()

        data1 = str1.current()

        recursive.level += 1
        max_match_rec(str1, str2, recursive)
        update_max_match(recursive.match, recursive.max_match)
        recursive.match = match_saved[:]
        assert recursive.level
        recursive.level -= 1

        str1.reset(data1)
        assert str1.can_advance()
        str1.advance()
        str2.reset(data2_saved)
        # if recursive.debug:
        #     print("max_match_rec_04", str1, str2, recursive.match)


def find_max_match(str1, str2, debug=False):
    '''determine the maximum submatch string between the two'''

    s_rec_1 = StringRec(str1)
    s_rec_2 = StringRec(str2)
    max_possible = s_rec_1.max_possible(s_rec_2)
    if len(max_possible) <= 1:
        return max_possible

    if debug:
        print("find_max_match", s_rec_1, s_rec_2)
        print("max possible: ", len(max_possible), max_possible)
        print("start: ", datetime.datetime.now().time())
        print()

    # lists because strings are immutable
    rec_data = lambda: None  # noqa: E731 do not assign a lambda expression,
    #                                use a def
    rec_data.match = []
    rec_data.max_match = [max_possible[0]]
    rec_data.level = 0
    rec_data.debug = debug
    rec_data.start = time.time()

    max_match_rec(s_rec_1, s_rec_2, rec_data)
    if debug:
        print("Elapsed time:", int(time.time() - rec_data.start))

    # verify that it is contained in the max possible solution
    test_max_match = rec_data.max_match[:]
    test_max_match.sort()
    pos = 0
    for i in test_max_match:
        while i != max_possible[pos]:
            pos += 1

    return ''.join(rec_data.max_match)


def tests():
    '''
        tests for the current problem
    '''
    if 1:  # pylint: disable=using-constant-test
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

    # DGCGTRMZJRBAJJV
    # Elapsed time: 83.42077136039734 -> 10s after optimization 1
    if 0:  # pylint: disable=using-constant-test
        result = find_max_match(
            'WEWOUCUIDGCGTRMEZEPXZFEJWISRSBBSYXAYDFEJJDLEBVHHKS',
            'FDAGCXGKCTKWNECHMRXZWMLRYUCOCZHJRRJBOAJOQJZZVUYXIC', True)
        print(result)
        assert result == 'DGCGTRMZJRBAJJV'

    # more of 10 min and still working
    # max possible:  73 ABBBBCDDEEEEFFFGGHHIJJJKKLLLMMMNNNOOOPQQQRRRRSSSTTTT
    #                   UUVVVVWWWXXYYYYYYYZZZ
    # update_max_match EGYWYVSZYTERTJNMF 17
    # update_max_match EGKYEWVSZYTERTJNMF 18
    # max_match_rec_02 LGGYJWKTDHLXJRBJLRYEJWVSUFZKYHOIKBGTVUTTOCGMLEXWDSX
    #                  EBKRZTQUVCJNGKKRMUUBACVOEQKBFFYBUQEMYNENKYYGUZSP 308
    # update_max_match LGGKYEWVSZYTERTJNMF 19
    if 1:  # pylint: disable=using-constant-test
        result = find_max_match(
            'ELGGYJWKTDHLXJRBJLRYEJWVSUFZKYHOIKBGTVUTTOCGMLEXWDSXEBKRZTQU'
            'VCJNGKKRMUUBACVOEQKBFFYBUQEMYNENKYYGUZSP',
            'FRVIFOVJYQLVZMFBNRUTIYFBMFFFRZVBYINXLDDSVMPWSQGJZYTKMZIPEGMV'
            'OUQBKYEWEYVOLSHCMHPAZYTENRNONTJWDANAMFRX', True)
        print(result)

    # result = find_max_match('AquaVitae', 'AruTaVae', True)
    # print(result)


if __name__ == "__main__":
    tests()
