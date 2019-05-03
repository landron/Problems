'''
    http://www.hackerrank.com/challenges/maximize-it
        maximize sum((x*x) mod M), taking an x from each line

        tag_knapsack (?),   "Subset sum problem" / Combinatorial optimization

    Version 2016.16.05

    pylint, flake8
'''
import itertools
import io


def maxim_powers(sets, remainder):
    '''solve the problem: the entries are already normalized (powers, %M)'''
    sums = set()
    prev = set({0})
    for line in sets:
        sums = set()
        for j in itertools.product(line, prev):
            sums.add((j[0]+j[1]) % remainder)
        prev = sums
    return max(sums)


def read_and_solve_base(read_line_func):
    '''hackerrank test function: reading line parameter given'''
    (lines_no, remainder) = (int(x) for x in read_line_func().strip().split())
    sets = []
    for _ in range(lines_no):
        # ! skip the number of elements
        imp = [int(x) for x in read_line_func().strip().split(' ')[1:]]
        sets.append(set((lambda x: (x*x) % remainder)(i) for i in imp))
    result = maxim_powers(sets, remainder)
    print(result)


def read_and_solve():
    '''hackerrank test function'''
    return read_and_solve_base(input)


def read_and_solve_with_text(text):
    '''hackerrank test function'''
    buf = io.StringIO(text)
    return read_and_solve_base(buf.readline)


def maxim_direct(sets, remainder):
    '''solve the problem: the entries are the ones directly given'''
    sums = set()
    prev = set({0})
    for line in sets:
        sums = set()
        for j in itertools.product(line, prev):
            sums.add((j[0]*j[0]+j[1]) % remainder)
        prev = sums
        print(sorted(sums))
    return max(sums)


def debug_validations():
    '''unit testing'''
    assert maxim_powers([{16, 25, 4}, {64, 9, 49, 81},
                         {64, 25, 49, 81, 100}], 1000) == 206
    assert maxim_powers([{16, 25}, {64, 49, 81},
                         {64, 25, 49, 81, 100}], 1000) == 206
    assert maxim_powers([{100, 287}, {685, 654}, {105}, {560, 64, 536, 295},
                         {417, 295}, {225, 66, 712, 121, 94}], 767) == 763
    assert maxim_powers([{3234, 533, 985, 954, 798, 542}, {291, 988, 413, 886},
                         {688, 233, 101}], 998) == 974
    assert maxim_powers([{24, 48, 96}, {24, 48, 96, 24}], 24) == 0


def main():
    '''main function: accessible from exterior'''
    debug_validations()
    read_and_solve_with_text("3 998\n"
                             "6 67828645 425092764 242723908 669696211"
                             "501122842 438815206\n"
                             "4 625649397 295060482 262686951 815352670\n"
                             "3 100876777 196900030 523615865")


if __name__ == "__main__":
    main()
