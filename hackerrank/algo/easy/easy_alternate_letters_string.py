'''
    https://www.hackerrank.com/challenges/two-characters/problem
        find the maximum alternate two letters substring (by eliminating letters)
'''

#!/bin/python3

import sys
from collections import OrderedDict

DEBUG = 1

def eliminate_consecutive_characters(s):
    prev = 0
    eliminate = []
    for i in s:
        if i == prev:
           eliminate.append(i) 
        prev = i
    while eliminate:
        for j in eliminate:
            s = s.replace(j, '')
        eliminate = []
        prev = 0
        for i in s:
            if i == prev:
                eliminate.append(i)
            prev = i
    return s

def is_solution(s):
    if len(s) < 2:
        return False
    first = s[0]
    second = s[1]
    prev = second
    for i in s:
        if i == first:
            if prev != second:
                return False
        elif i == second: 
            if prev != first:
                return False
        else:
            return False
        prev = i
    return True

def find_max_alternate_string(s, print_it = False):
    if DEBUG and print_it:
        print("\nStart:")
        print(s)

    s = eliminate_consecutive_characters(s)
    if len(s) < 2:
        return ""
    elif is_solution(s):
        return s

    if DEBUG and print_it:
        print(s)

    all = {}
    for i in s: 
        if i not in all:
            all[i] = 0
        all[i] += 1
    assert len(all) > 2

    letters_ascending = OrderedDict(sorted(all.items(), key=lambda kv: kv[1]))

    if DEBUG and print_it:
        print(letters_ascending)

    found = ""
    # bug: avoid early exit
    found_level_i = 0

    values = list(letters_ascending.keys())
    size = len(values)
    for i in range(size):
        val_i = values[size-i-1]
        cnt_i = all[val_i]

        if found_level_i != 0 and found_level_i != cnt_i:
            break

        for j in range(i+1, size):
            val_j = values[size-j-1]            
            cnt_j = all[val_j]
            assert cnt_i >= cnt_j
            # can they alternate ?
            if cnt_i - cnt_j > 1:
                break

            if DEBUG and print_it:
                print(val_i, val_j, cnt_i, cnt_j)

                t = s
                for k in s:
                    if k != val_i and k != val_j:
                        t = t.replace(k, '')
                print(t)

            solution = ""
            prev = 0            
            for k in s:
                if k == val_i:
                    if prev != 0 and prev != val_j:
                        solution = ""
                        break
                    prev = val_i
                elif k == val_j:
                    if prev != 0 and prev != val_i:
                        solution = ""
                        break
                    prev = val_j
                else:
                    continue
                solution += prev

            if solution:
                assert len(solution) == cnt_i+cnt_j
                # print(solution)
                if len(solution) > len(found):
                    found_level_i = cnt_i
                    found = solution

    return found

def twoCharacters(s):
    # Complete this function
    solution = find_max_alternate_string(s)
    return len(solution)

def tests():
    assert eliminate_consecutive_characters("abhhbr") == "ar"
    assert is_solution("ababab") == True
    assert is_solution("abababb") == False
    assert is_solution("abaabab") == False
    assert find_max_alternate_string("beabeefeab") == "babab"
    assert find_max_alternate_string("abaacdabd") == "bdbd"
    assert twoCharacters("h") == 0
    next = "cwomzxmuelmangtosqkgfdqvkzdnxerhravxndvomhbokqmvsfcaddgxgwtpgpqrmeoxvkkjunkbjeyteccpugbkvhljxsshpoymkryydtmfhaogepvbwmypeiqumcibjskmsrpllgbvc"
    assert len(eliminate_consecutive_characters(next)) == 105
    assert find_max_alternate_string(next) == "ujujujuj"
    next = "pvmaigytciycvjdhovwiouxxylkxjjyzrcdrbmokyqvsradegswrezhtdyrsyhg"
    assert not find_max_alternate_string(next) == "seses"
    assert find_max_alternate_string(next) == "icicic"
    next = "muqqzbcjmyknwlmlcfqjujabwtekovkwsfjrwmswqfurtpahkdyqdttizqbkrsmfpxchbjrbvcunogcvragjxivasdykamtkinxpgasmwz"
    assert find_max_alternate_string(next) == "nxnxnx"

if __name__ == "__main__":
    if DEBUG:
        tests()
    else:
        l = int(input().strip())
        s = input().strip()
        result = twoCharacters(s)
        print(result)