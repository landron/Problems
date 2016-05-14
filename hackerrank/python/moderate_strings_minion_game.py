'''
    http://www.hackerrank.com/challenges/the-minion-game

    Version 2016.05.14

    >pylint --version
        No config file found, using default configuration
        pylint 1.5.5,
        astroid 1.4.5
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10

    OPT:    maybe add a time-out case
'''

def play_1(string):
    '''solve the game: first variant, time-outs'''
    vowels = consonants = 0
    for i, _ in enumerate(string):
        for j in range(len(string)-i):
            if string[j] in "AEIOU":
                vowels += 1
            else:
                consonants += 1
    return (vowels, consonants)

def play_2(string):
    '''solve the game: still 4 time-outs'''
    vowels_total = consonants_total = 0
    for i, j in enumerate(string):
        if j in "AEIOU":
            vowels_total += 1
        else:
            consonants_total += 1
    vowels_game = consonants_game = 0
    for i, _ in enumerate(string):
        vowels = vowels_total
        consonants = consonants_total
        for j in range(len(string)-i, len(string)):
            if string[j] in "AEIOU":
                vowels -= 1
            else:
                consonants -= 1
        vowels_game += vowels
        consonants_game += consonants
    return (vowels_game, consonants_game)

def play_3(string):
    '''solve the game: the good solution'''
    vowels = consonants = 0
    for i, j in enumerate(string):
        if j in "AEIOU":
            vowels += (len(string)-i)
        else:
            consonants += (len(string)-i)
    return (vowels, consonants)

def play(string):
    '''solve the game'''
    return play_3(string)

def read_and_solve():
    '''Hackerrank test function'''
    game = input().strip()
    (vowels, consonants) = play(game)
    if vowels == consonants:
        print("Draw")
    elif vowels > consonants:
        print("Kevin", vowels)
    else:
        print("Stuart", consonants)

def debug_validations():
    '''unit testing'''
    play_func = [play, play_1, play_2, play_3]
    for func in play_func:
        assert func("AEIORU") == (19, 2)
        assert func("BANANA") == (9, 12)
        assert func("ANANAN") == (12, 9)
        assert func("UHTI") == (5, 5)

def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()
    # print(play("UHTI"))

if __name__ == "__main__":
    main()
