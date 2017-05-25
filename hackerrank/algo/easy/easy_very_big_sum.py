# https://www.hackerrank.com/challenges/a-very-big-sum

import sys

#n = int(input().strip())
#arr = [int(arr_temp) for arr_temp in input().strip().split(' ')]
arr = [1000000001, 1000000002, 1000000003, 1000000004, 1000000005]
# arr = [1111111111, 1111111112, 1111111113, 1111111114, 1111111115]

result = ""
while 0 != sum(arr):
	last = 0
	for i in range(len(arr)):
		last += arr[i]%10
		arr[i] //= 10
	arr.append(last//10)
	result = chr(ord('0')+last%10) + result
print(result)