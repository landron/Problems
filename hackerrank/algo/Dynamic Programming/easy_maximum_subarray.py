'''
    http://www.hackerrank.com/challenges/maxsubarray
         find the maximum possible sum of a contiguous subarray
    Version 2016.08.05

    >pylint --version
        No config file found, using default configuration
        pylint 1.5.5,
        astroid 1.4.5
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10
'''

# keeping the current sum IF positive is enough
def find_max_subarrays(arr):
    '''the solver function
            the trick is to keep it simple (calculate the partial sum all the time)
    '''
    assert len(arr) != 0

    sum_curr = sum_positives = max_seq = 0
    first_positive = -1
    for i, _ in enumerate(arr):
        if arr[i] >= 0:
            sum_positives += arr[i]
            if first_positive < 0 and arr[i] != 0:
                first_positive = i
            if sum_curr < 0:
                sum_curr = 0
        elif sum_curr > max_seq:
            max_seq = sum_curr
        sum_curr += arr[i]

    if first_positive == -1:
        maximum = max(arr)
        return (maximum, maximum)
    elif sum_curr > max_seq:
        max_seq = sum_curr

    assert sum_positives != 0 and max_seq != 0
    return (max_seq, sum_positives)

def read_and_solve():
    '''hackerrank input interface'''
    tests_no = int(input().strip())
    for _ in range(tests_no):
        _ = int(input().strip())
        array = [int(arr_temp) for arr_temp in input().strip().split(' ')]
        (sum1, sum2) = find_max_subarrays(array)
        print(sum1, sum2)

def read_and_solve_input_1():
    '''hackerrank missed test case'''
    file = open('input01.txt', 'r')
    tests_no = int(file.readline())
    for _ in range(tests_no):
        file.readline()
        arr_str = file.readline()
        array = [int(arr_temp) for arr_temp in arr_str.strip().split(' ')]
        (sum1, sum2) = find_max_subarrays(array)
        print(sum1, sum2)

def debug_validations():
    '''unit testing'''
    assert find_max_subarrays([-3, -1, 0, -5]) == (0, 0)
    assert find_max_subarrays([-3, -1, -5]) == (-1, -1)
    assert find_max_subarrays([2, -1, 2, 3, 4, -5]) == (10, 11)
    assert find_max_subarrays([1, 2, 3, 4]) == (10, 10)
    assert find_max_subarrays([-1, 1, 2, 3, 4]) == (10, 10)

    # bugs
    assert find_max_subarrays([9, -4, 2, -5, 8, -3, 2]) == (10, 21)
    assert find_max_subarrays([9, -4, 2, -5, 8, -4, 3, -1, 8]) == (16, 30)
    assert find_max_subarrays([9, -4, 2, -5, 3, 3, 2, -4, 3, -1, 1, 0, 3, 4]) == (16, 30)
    assert find_max_subarrays([9, -4, 2, -5, 3, 3, 3, -2, 0, -2, 3]) == (11, 23)
    assert find_max_subarrays([9, -4, 2, -5, 3, 3, 2, -2, 0, -2, 3, -2, 1, -1, 0, 3, 6]) == (16, 32)

def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()
    # read_and_solve_input_1()
    # array = [9, -4, 2, -5, 3, 3, 2, -2, 0, -2, 3, -2, 1, -1, 0, 3, 6]
    # print(array, find_max_subarrays(array))

if __name__ == "__main__":
    main()
