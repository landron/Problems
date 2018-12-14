#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/common-child/problem

    tag_class
    tag_string_match
'''


class StringRec():
    '''
        structure used for the recursivity match search:
            - str : immutable
    '''
    def __init__(self, string, dic_letters):
        assert string

        self.str = string
        self.dic = dic_letters
        self.pos = 0

    def __str__(self):
        # return self.str[self.pos:]
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
        self.dic = data[1]


def max_match_rec(str1, str2, match, max_match, level):
    '''
        determine recursively the maximum submatch string between the
         two entries
    '''
    if level == 1:
        print("max_match_rec_in", str1, str2)

    def update_match(str1, str2, match):
        assert str1.next() == str2.next()
        match += str1.next()
        str1.advance()
        str2.advance()

    def can_advance(str1, str2):
        return str1.can_advance() and str2.can_advance()

    while str1.next() == str2.next():
        update_match(str1, str2, match)
        assert match

        if not can_advance(str1, str2):
            return

    data2 = str2.current()
    # match is immutable inside the loop

    while True:
        # print("max_match_rec_02", str1, str2)

        while str1.can_advance() and not str2.contains(str1.next()):
            str1.advance()
        if not str1.can_advance():
            break

        while str2.next() != str1.next():
            assert str2.can_advance(), "the second string should contain '{0}'.\
                ".format(str1.next())
            str2.advance()

        data1 = str1.current()

        next_match = match[:]
        max_match_rec(str1, str2, next_match, max_match, level+1)
        if len(next_match) > len(max_match):
            # print(next_match)
            max_match[:] = next_match

        str1.reset(data1)
        if not str1.can_advance():
            break
        str1.advance()
        str2.reset(data2)
        # print("max_match_rec_04", str1, str2)


def find_max_match(str1, str2):
    '''determine the maximum submatch string between the two'''
    dic1 = 128 * [0]
    dic2 = 128 * [0]
    for i in str1:
        dic1[ord(i)] += 1
    for i in str2:
        dic2[ord(i)] += 1

    def max_possible(str1, str2):
        max_match = ''
        for i, val in enumerate(str1.dic):
            if val and str2.contains(chr(i)):
                for _ in range(min(val, str2.dic[i])):
                    max_match += chr(i)
        return max_match

    s_rec_1 = StringRec(str1, dic1)
    s_rec_2 = StringRec(str2, dic2)
    print("find_max_match", s_rec_1, s_rec_2)
    max_match = max_possible(s_rec_1, s_rec_2)
    print("max possible: ", len(max_match), max_match)

    # lists because strings are immutable
    match = []
    max_match = []

    max_match_rec(s_rec_1, s_rec_2, match, max_match, 0)
    if len(match) > len(max_match):
        max_match[:] = match
    return ''.join(max_match)


def tests():
    '''
        tests for the current problem
    '''
    if 0:  # pylint: disable=using-constant-test
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

    # WEWOCUIC
    result = find_max_match(
        'WEWOUCUIDGCGTRMEZEPXZFEJWISRSBBSYXAYDFEJJDLEBVHHKS',
        'FDAGCXGKCTKWNECHMRXZWMLRYUCOCZHJRRJBOAJOQJZZVUYXIC')
    print(result)


if __name__ == "__main__":
    tests()
