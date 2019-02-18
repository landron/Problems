#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/validating-credit-card-number

    Reference
        https://github.com/landron/Problems/blob/public-master/hackerrank/python/easy_regex_uid.py

    pylint, flake8

    tag_regex
'''
import re


def is_credit_card(candidate):
    '''
        ?= Matches if ... matches next, but doesn’t consume any of the string.
        ?! Matches if ... doesn’t match next. This is a negative lookahead
        assertion.

        Rules:
        1.  It must contain exactly 16 digits.
            It must only consist of digits (-).
        2.  It may have digits in groups of , separated by one hyphen "-".
        3.  It must start with a 4,5 or 6.
        4.  It must NOT have 4 or more consecutive repeated digits.
                Attention! \\1 must identify the correct group, the first
                (so the rule cannot be added last)

        It can be done with several matches instead of this big expression
    '''
    reg_expr = (r'(?!.*?(.)(-?\1){3})'               # Rule 4
                r'((?=([0-9]{16}$))'                 # Rule 1
                r'|'
                r'(?=([0-9]{4}-){3}[0-9]{4}$))'      # Rule 2
                r'(?=[456].+)'                       # Rule 3
                )
    return re.match(reg_expr, candidate)


def parse_input():
    '''
        parse input in HackerRank format
    '''
    no_lines = int(input().strip())
    for _ in range(no_lines):
        source = input().strip()
        if is_credit_card(source):
            print('Valid')
        else:
            print('Invalid')


def tests():
    '''
        tests for the current problem
    '''
    assert is_credit_card('4123456789123456')
    assert is_credit_card('4443456789122256')
    assert is_credit_card('4123-4567-8912-3456')
    assert not is_credit_card('4123-4567-8912_3456')
    assert not is_credit_card('4123-4567-891-93456')
    assert not is_credit_card('4123-4567-89123456')
    assert not is_credit_card('4123-4567-8912-3456-')
    assert not is_credit_card('7123456789123456')
    assert not is_credit_card('4123456711113456')
    assert is_credit_card('4123-4567-8912-2256')
    assert not is_credit_card('4123-4567-8922-2256')


if __name__ == "__main__":
    tests()
