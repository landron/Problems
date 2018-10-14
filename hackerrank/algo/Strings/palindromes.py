#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/special-palindrome-again/problem

    tough enough because of the organization (design):
        \todo did not chose the best design - keep a sequence and translate it
        (too much ifs)

    tag_string
'''


def calculate(cnt_prev, cnt_after, print_it=False):
    '''calculate the number of palindromes for a sequence'''
    palindroms_nb = 0

    # first one alone
    palindroms_nb += cnt_prev*(cnt_prev-1)//2
    # keep it for later as it can still participate to palindroms
    # palindroms_nb += cnt_after*(cnt_after-1)//2

    # combined
    palindroms_nb += cnt_after if cnt_after < cnt_prev else cnt_prev

    if palindroms_nb and print_it:
        print("calculate:", cnt_prev, cnt_after, palindroms_nb)

    return palindroms_nb


def substrCount(size_string, string):
    '''
        calculate the number of palindromes for the entire string
        accumulate as much as possible in a sequence, than calculate it
    '''
    assert size_string == len(string)

    print_it = False
    if print_it:
        print(string)

    palindroms_nb = 0

    prev = None
    cnt_prev = 0
    cnt_after = 0
    curr = None
    cnt_curr = 0

    for i in string:
        if print_it:
            print(i, "in:", cnt_prev, cnt_curr, cnt_after)
            print(prev, curr)

        if i == prev:
            cnt_after += 1
        elif i == curr:
            if cnt_after != 0:
                palindroms_nb += calculate(cnt_prev, cnt_after, print_it)
                cnt_prev = cnt_after
                cnt_curr = 1

                cnt_after = 1 if cnt_after == 1 else 0
                if cnt_after == 1:
                    curr, prev = prev, curr
            else:
                palindroms_nb += calculate(cnt_prev, 0, print_it)
                prev = None
                cnt_prev = 0
                cnt_curr += 1
        else:
            if cnt_after != 0:
                palindroms_nb += calculate(cnt_prev, cnt_after, print_it)
                cnt_prev = cnt_after
            else:
                palindroms_nb += calculate(cnt_prev, 0, print_it)
                cnt_prev = cnt_curr
                prev = curr
            curr = i
            cnt_curr = 1
            cnt_after = 0

        assert prev != curr

        if print_it:
            print(i, "out:", cnt_prev, cnt_curr, cnt_after)
            print(prev, curr)

    if cnt_after or cnt_prev:
        palindroms_nb += calculate(cnt_prev, cnt_after, print_it)
        palindroms_nb += calculate(cnt_after, 0, print_it)
    else:
        palindroms_nb += calculate(cnt_curr, 0, print_it)

    # trivials: letters
    palindroms_nb += len(string)

    return palindroms_nb


def palindroms(string):
    '''calculate the number of palindroms for this string'''
    return substrCount(len(string), string)


def from_file(file_path):
    '''read test from file'''
    with open(file_path) as file:
        string_size = int(file.readline().strip())
        string = file.readline().strip()
        assert string_size == len(string)
        return (string_size, string)


def debug_assertions():
    '''
        unit tests
    '''
    assert palindroms("ono") == 4
    assert palindroms("onop") == 5
    assert palindroms("onop") == 5
    assert palindroms("onopo") == 7
    assert palindroms("nonopo") == 9
    assert palindroms("onopoo") == 9
    assert palindroms("mnonopo") == 10
    assert palindroms("mnonopoo") == 12

    assert palindroms("asasd") == 7  # asa, sas

    assert palindroms("abcbaba") == 10

    assert palindroms("aab") == 4
    assert palindroms("aaba") == 6
    assert palindroms("aaaa") == 10
    assert palindroms("aaaab") == 11
    assert palindroms("aaaaba") == 13

    assert palindroms("aabaa") == 9
    assert palindroms("aabaab") == 10
    assert palindroms("aabaac") == 10
    assert palindroms("aabaaba") == 12
    assert palindroms("aabaaca") == 12

    assert palindroms("abbaa") == 7


def tests():
    '''
        main debugging function
    '''
    debug_assertions()
    # string_size, string = from_file("input02.txt")
    # n = substrCount(string_size, string) # 1272919
    # print(n)


if __name__ == '__main__':
    tests()
