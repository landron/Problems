# http://www.hackerrank.com/challenges/diagonal-difference
# http://stackoverflow.com/questions/181543/what-is-the-problem-with-reduce

def calculate_diff_1(a):
    n = len(a)

    sum1 = sum2 = 0
    for i in range(n):
        sum1 += a[i][i]
        sum2 += a[i][n-i-1]
    result = sum1-sum2
    if result < 0:
        result = -result
    return result

def calculate_diff_2(a):
    n = len(a)
    result = sum([a[i][i] for i in range(n)]) - sum([a[i][n-i-1] for i in range(n)])
    if result < 0:
        result = -result
    return result

def calculate_diff_3(a):
    n = len(a)
    result = sum(a[i][i] for i in range(n)) - sum(a[i][n-i-1] for i in range(n))
    if result < 0:
        result = -result
    return result

def calculate_diff_4(a):
    n = len(a)
    result = sum(a[i][i]-a[i][n-i-1] for i in range(n))
    if result < 0:
        result = -result
    return result

def calculate_diff(a):
    # return calculate_diff_1(a)
    return calculate_diff_4(a)

def read_input():
    n = int(input().strip())
    a = []
    for _ in range(n):
        a_t = [int(a_temp) for a_temp in input().strip().split(' ')]
        a.append(a_t)
    return a

def main():
    a = read_input()
    print(calculate_diff(a))

if __name__ == "__main__":
    main()
