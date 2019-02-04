#!/bin/python3
'''
    Purpose
       "In other words, find the minimum distance between any pair of equal
    elements in the array."
        https://www.hackerrank.com/challenges/minimum-distances

    6
    7 1 3 4 1 7
    =>
    3

    flake8
'''


def distance(first, second):
    return first-second if first > second else second-first


n = int(input().strip())
A = [int(A_temp) for A_temp in input().strip().split(' ')]

list_pos = []
for i in range(n):
    list_pos.append((i, A[i]))
list_pos.sort(key=lambda tup: tup[1])

dmin = n+1
i = 0
while i < n:
    val = list_pos[i][1]
    j = i + 1
    while j < n and list_pos[j][1] == val:
        for k in range(i, j):
            d = distance(list_pos[j][0], list_pos[k][0])
            if d < dmin:
                dmin = d
        j += 1
    i = j
print(dmin) if dmin != n+1 else print(-1)
