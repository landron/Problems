#!/bin/python3

'''
    https://www.hackerrank.com/challenges/a-chessboard-game-1/problem

    adapt external coordinates to internal ones:
        - starting from 0
        - inverse x, y coordinates

    wrong solution:
        trying to complete all the table by moving the piece ("knight jumps")
            a change entrain changes for the the possible moves, recursively: a single step is not enough

    good solution:
        just recurse and complete the table as needed

    optimization:
        keep the calculated table for multiple tests
'''

import time

# table goes from 0 to BOARD_SIZE-1 inside the program, +1 outside; x, y inverted: see chessboardGame
BOARD_SIZE = 16

# common code

def move(x, y, m):
    if m == 1:
        return (x-2, y+1)
    elif m == 2:
        return (x-2, y-1)
    elif m == 3:
        return (x+1, y-2)
    elif m == 4:
        return (x-1, y-2)
    else:
        return (-1, -1)

def move_allowed(x, y, m):
    (x1, y1) = move(x, y, m)
    if x1 >= 0 and y1 >= 0 and BOARD_SIZE > x1 and BOARD_SIZE > y1:
        return (x1, y1)
    return (-1, -1)

def can_move(x, y):
    for i in range(4):
        (x1, _) = move_allowed(x, y, i+1)
        if x1 >= 0:
            return True
    return False

def print_table(table):
    print()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            print('{0:2d} '.format(table[j][i]), end='')
        print()
    print()

# 2 = the second player wins, 1 = the first player wins
def solve_move(x, y, table):
    if table[x][y] != 0:
        return table[x][y]

    result = 2 # pessimistic
    for i in range(4):
        (x1, y1) = move_allowed(x, y, i+1)
        if x1 >= 0:
            if table[x1][y1] == 0:
                table[x1][y1] = solve_move(x1, y1, table)
            # the second wins by the next move, so the first (me) wins now
            if table[x1][y1] == 2:
                result = 1
                break
    table[x][y] = result

    return result

def chessboard_game_2(x, y):
    table = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    _ = solve_move(x, y, table)
    if 0:
        print_table(table)
    assert table[x][y] != 0
    return "First" if table[x][y] == 1 else "Second"

####################################################################################################
# failed solution code:
#   the table has to be complete with (some kind) of recurssion, a single step does not suffice

def move_inv(x, y, m):
    if m == 1:
        return (x+2, y-1)
    elif m == 2:
        return (x+2, y+1)
    elif m == 3:
        return (x-1, y+2)
    elif m == 4:
        return (x+1, y+2)
    else:
        return (-1, -1)

def move_inv_allowed(x, y, m):
    (x1, y1) = move_inv(x, y, m)
    if x1 >= 0 and y1 >= 0 and BOARD_SIZE > x1 and BOARD_SIZE > y1:
        return (x1, y1)
    return (-1, -1)

def completed(table):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if table[i][j] == 0:
                return False
            assert table[i][j] >= 2
    return True

# this does not work: changing one value also has to (recursively) change the dependent ones
def complete(table):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if not can_move(i, j):
                table[i][j] = 2

    step = 2
    while not completed(table):
        if 0:
            print(table)
            time.sleep(1)

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if table[i][j] == step:
                    for k in range(4):
                        (x, y) = move_inv_allowed(i, j, k+1)
                        if x >= 0:
                            if 0:
                                if x == 7 and y == 7:
                                    print(step, table[x][y])
                            if table[x][y] == 0:
                                table[x][y] = step+1
                            # we want to change parity if possible: if odd, first player wins
                            else:
                                parity = table[x][y]%2
                                if parity%2 == 0:
                                    table[x][y] = step+1
        step += 1

def chessboard_game_1(x, y):
    table = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    assert not completed(table)
    complete(table)
    print_table(table)
    assert completed(table)

    return "First" if table[x][y]%2 == 1 else "Second"

###############################################################

def chessboardGame(x, y):

    #
    # transform to program coordinates

    x -= 1
    y -= 1
    assert(x < BOARD_SIZE and y < BOARD_SIZE)

    # x is y and viceversa
    x, y = y, x

    # return chessboard_game_1(x, y)
    return chessboard_game_2(x, y)

def tests():
    assert can_move(BOARD_SIZE, BOARD_SIZE)
    assert not can_move(0, 0)
    assert not can_move(1, 1)
    assert can_move(0, 2)
    assert chessboardGame(5, 2) == "Second"
    assert chessboardGame(5, 3) == "First"
    # chessboard_game_1 fails
    assert chessboardGame(8, 8) == "First"

if __name__ == "__main__":
    tests()

    print(chessboardGame(8, 8))
