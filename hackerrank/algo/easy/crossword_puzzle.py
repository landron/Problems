#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/crossword-puzzle/problem

    version: 2018.11.18

    \todo
        "Stop writing classes... "
        https://news.ycombinator.com/item?id=3717715

    tag_struct, tag_python_struct
'''
# import collections

# this is really a burden for changeable structures
# FillEntry = collections.namedtuple("FillEntry", "x y vertical length")


def prev_is_word(table, i, j, vertical):
    '''unused yet'''
    if vertical:
        return i and table[i-1][j] == '-'
    return j and table[i][j-1] == '-'


def match(table, word, to_fill_entry):
    '''can the word fill that entry ?'''
    assert len(word) == to_fill_entry.length

    size = len(word)
    for i in range(size):
        entry = table[to_fill_entry.y+i][to_fill_entry.x]\
                if to_fill_entry.vertical else\
                table[to_fill_entry.y][to_fill_entry.x+i]
        assert entry != '+'
        if entry not in ('-', word[i]):
            return False
    return True


def fill_entry(table, word, to_fill_entry):
    '''set the word to this entry'''
    assert len(word) == to_fill_entry.length
    x_coord = to_fill_entry.x
    y_coord = to_fill_entry.y
    for i, val in enumerate(word):
        if to_fill_entry.vertical:
            assert table[y_coord+i][x_coord] == '-' or \
                   table[y_coord+i][x_coord] == val
        else:
            assert table[y_coord][x_coord+i] == '-' or \
                   table[y_coord][x_coord+i] == val

    # print(word, to_fill_entry.x, to_fill_entry.y,
    #     to_fill_entry.vertical, to_fill_entry.length)

    if not to_fill_entry.vertical:
        table[y_coord] = table[y_coord][:x_coord] + word + \
            table[y_coord][(x_coord+len(word)):]
    else:
        for i, val in enumerate(word):
            assert table[y_coord][x_coord] == '-' or \
                   table[y_coord][x_coord] == val
            table[y_coord] = table[y_coord][:x_coord] + val + \
                table[y_coord][(x_coord+1):]
            y_coord += 1


def analyze_table(table):
    '''return a list of the entries to be filled'''
    to_fill = []

    def add_word(words, word):
        if word and word.length > 1:
            words.append(word)

    # identify horizontal entries

    current = None
    for i, _ in enumerate(table):
        for j, _ in enumerate(table[i]):
            if table[i][j] == '-':
                if not current:
                    # current = FillEntry(x=i, y=j, vertical=True, length=1)
                    current = lambda: None  # noqa: E731
                    current.y = i
                    current.x = j
                    current.vertical = False
                    current.length = 1
                else:
                    current.length += 1
            else:
                add_word(to_fill, current)
                current = None
        add_word(to_fill, current)
        current = None

    # identify vertical entries

    current = None
    for i, _ in enumerate(table):
        for j, _ in enumerate(table[i]):
            if table[j][i] == '-':
                if not current:
                    current = lambda: None  # noqa: E731
                    current.y = j
                    current.x = i
                    current.vertical = True
                    current.length = 1
                else:
                    current.length += 1
            else:
                add_word(to_fill, current)
                current = None
        add_word(to_fill, current)
        current = None

    return to_fill


def crossword_solve_unique_length(table, words, to_fill):
    '''solve trivial solutions: unique sized entries
    '''
    assert len(to_fill) == len(words)

    last_len = len(words[0])
    last_len_size = 1

    to_delete = []

    for i in range(1, len(words)):
        if last_len == len(words[i]):
            last_len_size += 1
        else:
            if last_len_size == 1:
                fill_entry(table, words[i-1], to_fill[i-1])
                to_delete.append(i-1)
            last_len = len(words[i])
            last_len_size = 1
    if last_len_size == 1:
        i = len(words)-1
        fill_entry(table, words[i], to_fill[i])
        to_delete.append(i)

    # remove the trivial solved entries

    for i, val in enumerate(to_delete):
        del words[val-i]
        del to_fill[val-i]


def crossword_puzzle_parsed_rec(table, words, to_fill):
    '''trying recursively all the solutions until one is found

        \todo treat words & to_fill as read-only
    '''
    for i, word in enumerate(words):
        for j, entry in enumerate(to_fill):
            if entry.length != len(word):
                return None

            if not match(table, word, entry):
                continue

            table_work = table[:]  # \perf
            fill_entry(table_work, word, entry)
            if len(words) == 1:
                return table_work

            del words[i]
            del to_fill[j]
            table_work = crossword_puzzle_parsed_rec(
                table_work, words, to_fill)
            if table_work:
                return table_work
            words.insert(i, word)
            to_fill.insert(j, entry)
    return None


def crossword_puzzle(table, words_str):
    '''
        base function variant
    '''
    words = words_str.split(';')

    to_fill = analyze_table(table)
    # print(len(to_fill))
    assert len(to_fill) == len(words)

    # for w in to_fill:
    #     print(w.x, w.y, w.vertical, w.length)

    # better to try fir first the little ones
    reverse = False
    words.sort(key=len, reverse=reverse)
    to_fill.sort(key=lambda x: x.length, reverse=reverse)

    crossword_solve_unique_length(table, words, to_fill)
    if not words:
        return table
    table_work = table[:]
    # for i in table_work:
    #     print(i)
    # print(words)
    return crossword_puzzle_parsed_rec(table_work, words, to_fill)


# Complete the crosswordPuzzle function below.
def crosswordPuzzle(crossword, words):  # pylint: disable=invalid-name
    '''
        base function to implement for hackerrank
    '''
    result = crossword_puzzle(crossword, words)
    for i in result:
        print(i)


def tests():
    '''
        tests for the current problem
    '''
    res = crossword_puzzle([
        "+-++++++++",
        "+-++++++++",
        "+-++++++++",
        "+-----++++",
        "+-+++-++++",
        "+-+++-++++",
        "+++++-++++",
        "++------++",
        "+++++-++++",
        "+++++-++++"],
                           # pylint weird alignment
                           "LONDON;DELHI;ICELAND;ANKARA")
    assert res

    res = crossword_puzzle([
        "+-++++++++",
        "+-++++++++",
        "+-------++",
        "+-++++++++",
        "+-++++++++",
        "+------+++",
        "+-+++-++++",
        "+++++-++++",
        "+++++-++++",
        "++++++++++"],
                           "AGRA;NORWAY;ENGLAND;GWALIOR")
    assert res

    res = crossword_puzzle([
        "+----+++++",
        "++++-+++++",
        "++++-+++++",
        "++++------",
        "++++-+++-+",
        "++++-+++-+",
        "++++-+++-+",
        "++++-+++-+",
        "++++-+++++",
        "++++++++++"],
                           "TREE;ELEPHANTS;PICKLE;LEMON")
    for i in res:
        print(i)


if __name__ == '__main__':
    tests()
