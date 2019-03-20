#!/usr/bin/env python3
# coding=utf-8
'''
    2018/03/20, 1:  24/28, 4 timeouts
    2018/03/20, 2:  26/28, 2 timeouts
        eliminate_massive added: it works well for equal values
    2018/03/20, 3:  done
        make another list with the new added values (as much as possible)
        append it, sort it (INSTEAD of inserting each value)

    Most other solutions used heapq .
        https://www.hackerrank.com/challenges/jesse-and-cookies

    tag_nice

    flake8, pylint
'''
import time
import bisect


def cross_threshold(threshold, arr_in, trace=False):
    '''
        increase all the variables above the given threshold,
        using the following algorithm:
            * new value = value[0] + 2 * value[1]
            * add "new value" to the list

        eliminate_massive reduced the timeout from 5min to 4s
    '''
    assert trace or not trace, "maybe not used"

    arr = sorted(arr_in)
    if arr[0] >= threshold:
        return 0

    def eliminate_massive(arr, new_val, threshold):
        next_vals = [new_val]
        i = 2
        while i+1 < len(arr) and arr[i] < threshold and arr[i+1] < new_val:
            val = arr[i] + 2*arr[i+1]
            if val < threshold:
                next_vals.append(val)
            i += 2

        del arr[0:i]
        next_vals.extend(arr)
        next_vals.sort()

        return next_vals, i//2

    steps = 0
    while len(arr) > 1:
        # print(arr)
        arr, inc = eliminate_massive(arr, arr[0] + 2*arr[1], threshold)
        # print(arr, inc)
        steps += inc

        if arr[0] >= threshold:
            return steps

    return -1


def cross_threshold_work(threshold, arr_in, trace=False):
    '''
        increase all the variables above the given threshold,
        using the following algorithm:
            * new value = value[0] + 2 * value[1]
            * add "new value" to the list

        UNUSED: solution built here
    '''
    # pylint: disable=too-many-statements

    arr = sorted(arr_in)
    if arr[0] >= threshold:
        return 0

    # eliminate already larger except one
    idx = bisect.bisect_left(arr, threshold)
    assert idx
    if idx < len(arr):
        arr = arr[0:idx+1]

    steps = 0

    # eliminate 0
    idx = bisect.bisect_right(arr, 0)
    if idx:
        steps += (idx-1)
        arr = arr[idx-1:]

    def eliminate_massive_equals(arr, size):
        if size % 2 == 1:
            size -= 1
        new_val = 3*arr[0]
        del arr[0:size]

        idx = bisect.bisect_right(arr, new_val)
        next_arr = arr[0:idx]
        next_arr.extend([new_val] * (size//2))
        next_arr.extend(arr[idx:])

        return next_arr, size//2

    def eliminate_massive(arr, new_val):
        next_vals = [new_val]
        i = 2
        while i+1 < len(arr) and arr[i+1] < new_val:
            val = arr[i] + 2*arr[i+1]
            if val < threshold:
                next_vals.append(val)
            i += 2
        del arr[0:i]

        if 0:  # pylint: disable=using-constant-test
            j = 0
            if len(arr) < 2:
                bisect.insort(arr, next_vals[0])
                j += 1
            while j < len(next_vals):
                if next_vals[j] > threshold:
                    break
                bisect.insort(arr, next_vals[j])
                j += 1
        else:
            next_vals.extend(arr)
            next_vals.sort()
            arr = next_vals

        return arr, i//2

    last = arr[0]
    while len(arr) > 1:
        idx_same = bisect.bisect_right(arr, arr[0])
        if idx_same > 3:
            arr, inc = eliminate_massive_equals(arr, idx_same)
            steps += inc
        else:
            new_val = arr[0] + 2*arr[1]

            # classic code
            # del arr[0:2]
            # if new_val < threshold or len(arr) < 2:
            #     bisect.insort(arr, new_val)
            # steps += 1

            # treat massive no 2
            # 300s -> 40s -> 4s
            arr, inc = eliminate_massive(arr, new_val)
            steps += inc

        if arr[0] >= threshold:
            return steps

        if trace:
            if 0 and last != arr[0]:
                last = arr[0]
                print("new first", arr[0])
            if not steps % 1000 or 1:
                print(steps, arr[0], len(arr))

    return -1


def parse_with(input_func, output_func):
    '''
        parse the HackerRank input
    '''
    size, threshold = (int(i) for i in input_func().strip().split())
    arr = [int(i) for i in input_func().strip().split()]
    print(threshold, size)
    if 1:  # pylint: disable=using-constant-test
        steps_no = cross_threshold(threshold, arr, True)
        print(steps_no)
        output_func(str(steps_no))
    else:
        arr.sort()
        for i in arr:
            output_func(str(i))
            output_func(' ')


def parse_big_test():
    '''
        parse some big file HackerRank input

        input21.txt:
            615271
            Tests in 295.93 seconds

            615271
            Tests in 40.20 seconds
                "treat massive no 2" branch

            615271
            Tests in 3.63 seconds
                sort instead of insort; the clean solution
    '''
    class PrettyFileWriter:
        '''
            "A Gentle Introduction to Context Managers:
                The Pythonic Way of Managing Resources"
            https://alysivji.github.io/managing-resources-with-context-managers-pythonic.html
            "subclassing file objects"
            https://stackoverflow.com/questions/16085292
        '''
        def __init__(self, fileName):
            self.file = open(fileName, 'w')

        def __enter__(self):
            # return self.file
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.file.close()

        def writenl(self, line):
            '''
                normal "write" function, but also add a new line
                    (the reason of this "subclassing", PrettyFileWriter)
            '''
            self.file.write(line)
            self.file.write('\n')

    start = time.time()

    fptr = open('input21.txt', 'r')
    # parse_with(fptr.readline, print)
    with PrettyFileWriter('output21-mine.txt') as fptr_w:
        parse_with(fptr.readline, fptr_w.writenl)
        # parse_with(fptr.readline, fptr_w.file.write)

    duration = time.time()-start
    if duration >= 1:
        print("Tests in {0:.2f} seconds".format(duration))


def tests():
    '''
        tests for the current problem

        pass -O to ignore assertions and gain some time:
            py -3 -O ./prob.py
    '''
    start = time.time()

    assert cross_threshold(7, [1, 2, 3, 9, 10, 12]) == 2
    assert cross_threshold(3, [1, 0, 0, 3]) == 3
    assert cross_threshold(2, [1, 0, 0]) == 2
    assert cross_threshold(71, [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])\
        == 14

    duration = time.time()-start
    if duration >= 1:
        print("Tests in {0:.2f} seconds".format(duration))


def main():
    '''main'''
    tests()
    # parse_big_test()

    # res = cross_threshold(7, [1, 2, 3, 9, 10, 12], True)
    # print(res)


if __name__ == "__main__":
    main()
