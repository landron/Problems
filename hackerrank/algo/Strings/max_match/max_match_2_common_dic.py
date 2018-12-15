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

    optimization 3: keep the maximum size in SizedDict
        this is even slower : 127s vs 83s
'''
import datetime
import time


class SizedDict():
    '''
        array of letters and the associated total number
    '''
    def __init__(self, string=''):
        # lowercase and uppercase ASCII
        self.dic = 128 * [0]
        self.count = 0
        for i in string:
            self.dic[ord(i)] += 1
            self.count += 1

    def __str__(self):
        # result = str(self.count) + ': '
        result = ''
        result += self.presentation()
        return result

    def presentation(self):
        '''get a nice represenation of this dictionary'''
        result = ''
        for i, val in enumerate(self.dic):
            result += chr(i)*val
        return result

    def contains(self, ch_next):
        '''does the string contains the character ?'''
        return self.dic[ord(ch_next)] > 0

    def can_advance(self):
        '''any interesting characters left ?'''
        return self.count != 0

    def decrement(self, ch_next):
        '''decrement the counter for this character'''
        assert self.contains(ch_next)
        self.dic[ord(ch_next)] -= 1
        assert self.count
        self.count -= 1

        return self.count != 0

    def update_to_min(self, other, ch_next):
        '''update the counter to the minimum of the other'''
        if self.contains(ch_next):
            pos = ord(ch_next)
            if self.dic[pos] > other.dic[pos]:
                count = self.dic[pos] - other.dic[pos]
                self.dic[pos] -= count
                assert self.count > count
                self.count -= count

    def reset_position(self, pos):
        '''reset the counter for the position'''
        assert self.count >= self.dic[pos] >= 0
        self.count -= self.dic[pos]
        self.dic[pos] = 0

    def copy(self):
        '''a copy of itself'''
        acopy = SizedDict()
        acopy.dic = self.dic[:]
        acopy.count = self.count
        return acopy

    def restore(self, copy):
        '''restore this object from the copy'''
        self.count = copy.count
        self.dic = copy.dic[:]


class StringRec():
    '''
        structure used for the recursivity match search:
            - str : immutable
    '''
    def __init__(self, string):
        assert string

        self.str = string
        self.pos = 0
        self.dic = SizedDict(string)

    def __str__(self):
        result = "("
        result += self.str[self.pos:]
        result += ", "
        # for i, val in enumerate(self.dic.dic):
        #     if val:
        #         result += chr(i)
        #         result += ':'
        #         result += str(val)
        #         result += ' '
        # result = result[:-1]
        result += str(self.dic)
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

    def reset(self, character):
        '''current character cannot be a match anymore'''
        return self.dic.reset_position(ord(character))

    def decrement(self):
        '''decrement counter for this character'''
        self.dic.decrement(self.next())

    def can_advance(self):
        '''have we reach the end of the string ?'''
        # return self.pos < len(self.str)
        assert not self.dic.can_advance() or self.pos < len(self.str)
        return self.dic.can_advance()

    def advance(self):
        '''increment: advance to the next character'''
        assert self.can_advance()

        if self.contains(self.next()):
            self.decrement()
        self.pos += 1

        return self.can_advance()

    def contains(self, ch_next):
        '''does the string contains the character ?'''
        return self.dic.contains(ch_next)

    def __seek(self, pos):
        assert pos < len(self.str)
        self.pos = pos

    def current(self):
        '''return the current mutable data'''
        return (self.pos, self.dic.copy())

    def restore(self, data):
        '''restore mutable data to restart the search'''
        self.__seek(data[0])
        self.dic.dic = data[1].dic[:]
        self.dic.count = data[1].count

    def max_possible(self, other):
        '''best match between those two strings'''
        max_match = SizedDict()
        for i, val in enumerate(self.dic.dic):
            if val and other.contains(chr(i)):
                max_match.dic[i] = min(val, other.dic.dic[i])
                max_match.count += max_match.dic[i]
        return max_match

    def reset_to_common(self, max_match):
        '''reset the dictionary to the values in given one'''
        for i, val in enumerate(max_match.dic):
            if not val:
                self.dic.reset_position(i)


def max_match_rec(str1, str2, recursive):
    '''
        determine recursively the maximum submatch string between the
         two entries
    '''
    if recursive.debug and recursive.level == 0:
        print("max_match_rec_in", str1, str2, recursive.max_match)

    def advance_first(max_match, str1, str2):
        ch_next = str1.next()

        str1.advance()
        max_match.update_to_min(str1.dic, ch_next)
        if not max_match.contains(ch_next):
            str2.reset(ch_next)

    def advance(max_match, str1, str2):
        ch_next = str1.next()
        assert ch_next == str2.next()

        str1.advance()
        str2.advance()

        if not max_match.decrement(ch_next):
            str1.reset(ch_next)
            str2.reset(ch_next)

    def can_advance(str1, str2):
        return str1.can_advance() and str2.can_advance()

    def update_match(match, best_match, ch_next=''):
        recursive.match += ch_next
        if len(match) > len(best_match):
            best_match[:] = match
            print("update_best_match", ''.join(best_match), len(best_match))

    def is_max_possible(recursive):
        result = len(recursive.best_match) < len(recursive.match) +\
            recursive.max_match.count
        # if not result:
        #     print("Optimization: ", len(recursive.best_match),
        #           len(recursive.match), max_possible)
        return result

    while str1.next() == str2.next():
        update_match(recursive.match, recursive.best_match, str1.next())
        advance(recursive.max_match, str1, str2)
        assert recursive.match

        if not can_advance(str1, str2):
            return

    if not is_max_possible(recursive):
        return

    data2_saved = str2.current()
    # match is immutable inside the loop
    match_saved = recursive.match[:]
    max_match_saved = recursive.max_match.copy()

    while True:
        if recursive.debug and recursive.level == 0:
            print("max_match_rec_02", str1.value(),
                  int(time.time() - recursive.start))

        while not recursive.max_match.contains(str1.next()) and str1.advance():
            pass
        if not str1.can_advance():
            break

        data1_saved = str1.current()

        while str2.next() != str1.next():
            advance_first(recursive.max_match, str2, str1)
            assert str2.can_advance(), "the second string should contain '{0}'.\
                ".format(str1.next())

        recursive.level += 1
        max_match_rec(str1, str2, recursive)
        update_match(recursive.match, recursive.best_match)
        recursive.match = match_saved[:]
        assert recursive.level
        recursive.level -= 1

        str1.restore(data1_saved)

        str2.restore(data2_saved)
        recursive.max_match.restore(max_match_saved)

        assert str1.can_advance()
        if not str1.advance():
            break


def find_max_match(str1, str2, debug=False):
    '''determine the maximum submatch string between the two'''

    s_rec_1 = StringRec(str1)
    s_rec_2 = StringRec(str2)
    max_possible = s_rec_1.max_possible(s_rec_2)
    if max_possible.count <= 1:
        return str(max_possible)

    s_rec_1.reset_to_common(max_possible)
    s_rec_2.reset_to_common(max_possible)

    if debug:
        print("find_max_match", s_rec_1, s_rec_2)
        print("max possible: ", max_possible.count, max_possible)
        print("start: ", datetime.datetime.now().time())
        print()

    # lists because strings are immutable
    rec_data = lambda: None  # noqa: E731 do not assign a lambda expression,
    #                                use a def
    rec_data.match = []
    rec_data.best_match = [str(max_possible)[0]]
    # \todo this is a good validation
    rec_data.max_match = max_possible.copy()
    rec_data.level = 0
    rec_data.debug = debug
    rec_data.start = time.time()

    max_match_rec(s_rec_1, s_rec_2, rec_data)
    if debug:
        print("Elapsed time:", int(time.time() - rec_data.start))

    # verify that it is contained in the max possible solution
    #   crash/assertion if there is a problem
    test_max_match = rec_data.best_match[:]
    test_max_match.sort()
    pos = 0
    max_possible_str = max_possible.presentation()
    for i in test_max_match:
        while i != max_possible_str[pos]:
            pos += 1

    return ''.join(rec_data.best_match)


def tests():
    '''
        tests for the current problem

        pass -O to ignore assertions and gain some time:
            py -3 -O ./prob.py
    '''
    # assert False

    if 1:  # pylint: disable=using-constant-test
        assert find_max_match('abc', 'def') == ''
        assert find_max_match('abc', 'dcf') == 'c'
        assert find_max_match('abcd', 'abdc') == 'abc'

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

    # 36s
    if 1:  # pylint: disable=using-constant-test
        result = find_max_match(
            'WEWOUCUIDGCGTRMEZEPXZFEJWISRSBBSYXAYDFEJJDLEBVHHKS',
            'FDAGCXGKCTKWNECHMRXZWMLRYUCOCZHJRRJBOAJOQJZZVUYXIC', True)
        print(result)
        assert result == 'DGCGTRMZJRBAJJV'

    if 0:  # pylint: disable=using-constant-test
        result = find_max_match(
            'ELGGYJWKTDHLXJRBJLRYEJWVSUFZKYHOIKBGTVUTTOCGMLEXWDSXEBKRZTQU'
            'VCJNGKKRMUUBACVOEQKBFFYBUQEMYNENKYYGUZSP',
            'FRVIFOVJYQLVZMFBNRUTIYFBMFFFRZVBYINXLDDSVMPWSQGJZYTKMZIPEGMV'
            'OUQBKYEWEYVOLSHCMHPAZYTENRNONTJWDANAMFRX', True)
        print(result)

    # result = find_max_match('ABCDEF', 'FBDAMN', True)
    # print(result)


if __name__ == "__main__":
    tests()
