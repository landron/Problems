#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/fraudulent-activity-notifications

    tag_binary_heap
    tag_counting_sort

    bisect.insort
        "Keep in mind that the O(log n) search is dominated by
        the slow O(n) insertion step."

    flake8
'''
import bisect

# not used because no remove support
# import heapq
#   \todo:  try to use heapq with an attached dictionary
#           https://stackoverflow.com/questions/13800947/deleting-from-python-heapq-in-ologn/
#   idea: keep components - heap-max, median, heap-min and update them => logn


def median(arr):
    pos = len(arr)//2
    if len(arr) % 2 == 1:
        med = arr[pos]
    else:
        med = (arr[pos-1] + arr[pos])/2.0
    # print(arr, med)
    return med


def activity_notifications_2_1(expenditure, d):
    '''
        this passes: deleting index >> removing element
    '''
    l_sorted = sorted(expenditure[:d])

    count = 0
    for i in range(d, len(expenditure)):
        med = median(l_sorted)
        # print(l_sorted, med, expenditure[i])
        if expenditure[i] >= 2*med:
            count += 1

        if expenditure[i-d] != expenditure[i]:
            del l_sorted[bisect.bisect_left(l_sorted, expenditure[i-d])]
            bisect.insort(l_sorted, expenditure[i])

    return count


def activityNotifications(expenditure, d):
    return activity_notifications_2_1(expenditure, d)


def tests():
    '''
        tests for the current problem
    '''
    assert activityNotifications([1, 2, 3, 4, 4], 4) == 0
    assert activityNotifications([2, 3, 4, 2, 3, 6, 8, 4, 5], 5) == 2
    assert activityNotifications([10, 20, 30, 40, 50], 3) == 1
    res = activityNotifications([2, 3, 4, 2, 3, 6, 8, 4, 5], 5)
    print(res)


if __name__ == '__main__':
    tests()
