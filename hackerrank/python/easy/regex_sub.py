#!/usr/bin/env python3
# coding=utf-8
'''
    tag_regex : ugly, ugly problem
'''
import re


def replace_logical_ops(line):
    '''
        replace C-like logical operators with equivalent words
    '''
    def replace_match(match):
        return "and" if "&&" in match.group(0) else "or"
    return re.sub(r"(?<= )(&&|\|\|)(?= )", replace_match, line)


def parse_input():
    '''
        treat HackerRank I/O
    '''
    lines_no = int(input().strip())
    for _ in range(lines_no):
        line = input()
        result = replace_logical_ops(line)
        print(result)


def tests():
    '''
        tests for the current problem

        pass -O to ignore assertions and gain some time:
            py -3 -O ./prob.py
    '''
    assert replace_logical_ops("&&") == "&&"
    assert replace_logical_ops(" && ") == " and "
    assert replace_logical_ops("|| || ") == "|| or "
    assert replace_logical_ops(" &&& && ||| ") == " &&& and ||| "


if __name__ == "__main__":
    tests()
