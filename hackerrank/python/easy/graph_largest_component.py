#!/bin/python3
'''
    https://www.hackerrank.com/challenges/friend-circle-queries/problem

    Version 2019.02.18
        14/15: timeout for test 10 (41.25/45: not all tests are considered)
        done: try to keep the tree equilibrate & add shortcuts

    flake8, pylint

    tag_graph_equlibrate
'''


def max_circle(shakes):
    '''
        shakes: list of edges
        return the list with the size of the maximum component at each step
    '''
    assert shakes

    result = [0]

    component = {}
    for _, shake in enumerate(shakes):
        comp1, comp2 = shake[1], shake[0]

        size1 = 0
        while comp1 in component and component[comp1][0]:
            comp1, _ = component[comp1]
            size1 += 1
        size2 = 0
        while comp2 in component and component[comp2][0]:
            comp2, _ = component[comp2]
            size2 += 1

        # improvement (?): try to keep the "components tree" equilibrate
        if size1 > size2:
            comp1, comp2 = comp2, comp1

        heigh_src = component[comp1][1] if comp1 in component else 1
        component[comp1] = (comp2, 0)
        heigh_dest = component[comp2][1] if comp2 in component else 1
        component[comp2] = (0, heigh_src+heigh_dest)

        # improvement: also shortcut the newly added entries
        if shake[0] not in component:
            component[shake[0]] = (comp2, 0)
        if shake[1] not in component:
            component[shake[1]] = (comp2, 0)

        # print(component)

        if heigh_src+heigh_dest > result[-1]:
            result.append(heigh_src+heigh_dest)
        else:
            result.append(result[-1])
    result.pop(0)

    return result


def parse_input():
    '''
        parse input in the HackerRank format
    '''


def tests():
    '''
        unit tests, assertions
    '''
    assert max_circle([(1, 2), (3, 4), (2, 3)]) == [2, 2, 4]
    assert max_circle([(1, 2), (1, 3)]) == [2, 3]
    assert max_circle([(1000000000, 23), (11, 3778), (7, 47),
                       (11, 1000000000)]) == [2, 2, 2, 4]
    assert max_circle([(1, 2), (3, 4), (1, 3), (5, 7), (5, 6),
                       (7, 4)]) == [2, 2, 4, 4, 4, 7]

    assert max_circle([(1, 2), (3, 1), (1, 7)]) == [2, 3, 4]

    # result = max_circle([(1, 2), (3, 4), (1, 3), (5, 7), (5, 6), (7, 4)])
    # print(result)


def main():
    '''main'''
    tests()
    # parse_input()


if __name__ == '__main__':
    main()
