'''
    https://www.hackerrank.com/challenges/making-candies/problem
        from "Interview Preparation Kit"
        (https://www.hackerrank.com/interview/interview-preparation-kit/search/challenges)

    What a beautiful problem!
'''


def minimum_passes_greedy(machines, workers, cost, target, debug):
    '''
        just try to keep machines and workers equal, to maximize their product
    '''
    def get_passes_no_more_buy(target, candies, production):
        if (target - candies) % production:
            return (target - candies) // production + 1
        return (target - candies) // production

    candies = machines*workers
    passes = 1
    passes_no_more_buy = 1 + get_passes_no_more_buy(
                            target, candies, machines*workers)
    if cost >= target:
        return passes_no_more_buy

    while candies < target:
        if candies < cost:
            new_passes = get_passes_no_more_buy(
                            cost, candies, machines*workers)
            candies += new_passes*machines*workers
            assert candies >= cost
            passes += new_passes

        buy = candies//cost
        candies -= buy*cost

        def next_mw(first, second, buy):
            assert first >= second
            if second + buy <= first:
                return (second + buy, first)
            buy -= (first-second)
            return (first + buy//2, first + buy - buy//2)

        # maximize product by keep them equal or close
        if machines >= workers:
            machines, workers = next_mw(machines, workers, buy)
        else:
            machines, workers = next_mw(workers, machines, buy)

        candies += machines*workers
        passes += 1
        if debug:
            print(f"{passes}. total={candies}, m,w={machines, workers}, "
                  f"no buy={passes_no_more_buy}")
        if passes >= passes_no_more_buy:
            passes = passes_no_more_buy
            break

        # optimization: maybe we can just keep current work load
        # Ex: cost=6, target=45, 25 candies, 4 machines workers
        candidate = passes + get_passes_no_more_buy(
                                target, candies, machines*workers)
        if candidate < passes_no_more_buy:
            passes_no_more_buy = candidate

    return passes


def minimum_passes(machines, workers, cost, target, debug=False):
    """
        * each step can produce machines*workers candies
        * candies can be sell to buy machines/workers for the cost
        * minimum number of passes to have target candies
    """
    return minimum_passes_greedy(machines, workers, cost, target, debug)


def debug_validations():
    """all the assertions"""
    assert minimum_passes(1, 2, 1, 60) == 4
    assert minimum_passes(3, 1, 2, 12) == 3
    assert minimum_passes(1, 1, 6, 45) == 16
    assert minimum_passes(499999, 1000000, 999996, 1000000000000) == 2
    assert minimum_passes(5361, 3918, 8447708, 989936375520) == 3577
    assert minimum_passes(7, 1, 456, 398) == 57
    assert minimum_passes(1, 1, 1000000000000, 1000000000000) == 1000000000000

    assert minimum_passes(1000000, 1, 440000000001, 1000000000000) == 940001


def main():
    """main"""
    debug_validations()
    # print(minimum_passes(1000000, 1, 440000000001, 1000000000000, True))


if __name__ == "__main__":
    main()
