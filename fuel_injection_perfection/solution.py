from time import time
from collections import Counter
from itertools import product
from math import log

def count_factors(n):
    ret = Counter()

    for i in range(2, int(n / 2)):
        while n % i == 0:
            ret[i] += 1
            n /= i

    if n > 1:
        ret[n] += 1

    return ret

#for i in range(200):
#    print("{}: {}".format(i, list_factors(i)))

def score1(n):
    score = 0

    upper_bound = 1
    while upper_bound < n:
        upper_bound *= 2
        score += 1

    if upper_bound == score:
        return score

    lower_bound = upper_bound / 2

    ret = score

    for i in range(lower_bound, n):
        pass

    #ret = min(
    #    n - i + score(i) for i in range(lower_bound, n)
    #)

    print("{}: {}".format(n, ret))
    return ret

scores = {}
numbers = {}

def score2(n):
    cur_score = 0
    cur_two_power = 1

    def print_score_list(s):
        l = sorted(scores[s], reverse=True)
        for i, n in enumerate(l):
            imod = (i + 1) / 2
            power = s - imod
            addition = -imod if (i % 2 == 0) else +imod
            if n != 2 ** power + addition:
                print("{}: {}".format(s, ["{:b}".format(n) for n in l]))
                return
        print("{}: good".format(s))


        # if s > 0:
        #     new_len = len(nums)
        #     prev_len = len(scores[s-1])
        #     if new_len - prev_len != 2:
        #         print("{}->{}: +{}".format(s-1, s, new_len - prev_len))
        #         prev_len = new_len

    def new_score(n, s):
        if s not in scores:
            scores[s] = set()
        scores[s].add(n)
        numbers[n] = s

    while n not in numbers:
        new_score(cur_two_power, cur_score)
        print_score_list(cur_score)

        for num in scores[cur_score]:
            for neighbour in (num + 1, num - 1):
                if neighbour > 0 and neighbour not in numbers:
                    new_score(neighbour, cur_score + 1)

        cur_score += 1
        cur_two_power *= 2

    return numbers.get(n)

def print_score_list(s, l):
    l = sorted(l, reverse=True)
    print("{}: {}".format(s, ["{:}".format(n) for n in l]))
    # if(s > 0 and len(scores[s]) - len(scores[s-1]) != 2):
    #     print("{}: {}".format(s, len(scores[s])))

def get_numbers1(score, number=None):
    scores = {}
    numbers = {}
    paths = {}

    def new_score(n, s):
        if s not in scores:
            scores[s] = set()
        if n in numbers:
            print("Tried to set {} to {} (already set as {})".format(
                n,
                s,
                numbers[n]
            ))
        scores[s].add(n)
        numbers[n] = s

    new_score(1, 0)

    cur_score = 0

    if number:
        cont_check = lambda s: number not in numbers
    else:
        cont_check = lambda s: s <= score

    while cont_check(cur_score):
        for num in scores[cur_score]:
            for op, neighbour in (
                ("-1", num + 1),
                ("+1", num - 1),
                ("/2", num * 2)
            ):
                if neighbour > 0 and neighbour not in numbers:
                    paths[neighbour] = (op, num, paths.get(num))
                    new_score(neighbour, cur_score + 1)
        cur_score += 1

    return (numbers[number], paths.get(number)) if number else set(scores[score])

def get_score1(number):
    return get_numbers1(None, number)

def get_numbers2(score):
    if score == 0:
        return { 1 }

    if score == 1:
        return { 2 }

    ret = []

    def get_count(score):
        sub = 1
        i = 1

        while i + sub < score:
            sub += 1
            i *= 2

        return (score - sub) * 2

    for i in range(get_count(score)):
        imod = (i + 1) // 2
        power = score - imod
        addition = -imod if (i % 2 == 0) else +imod
        ret.append(2 ** power + addition)

    return set(ret)

def get_score2(n):
    n = int(n)

    score = 0

    while n % 2 == 0:
        n /= 2
        score += 1

    floor_score = int(log(n, 2))
    floor_two_power = 2 ** floor_score

    ceil_score = floor_score + 1
    ceil_two_power = floor_two_power * 2

    return score + min(
        ceil_score + (ceil_two_power - n),
        floor_score + (n - floor_two_power)
    )

def get_score3(n):
    n = int(n)

    score = 0

    while n != 1:
        if n == 3:
            n -= 1
            score += 1
        elif n % 2 != 0:
            if (n + 1) % 4 == 0:
                n += 1
                score += 1
            else:
                n -= 1
                score += 1
        while n % 2 == 0:
            n /= 2
            score += 1
    return score

for i in range(1, 400):
    actual, path = get_score1(i)
    guess= get_score3(i)
    if actual != guess:
        print("(guess {} actual {}) {} -> {}".format(guess, actual, i, path))

# from sympy import sieve
# from sympy.ntheory import factorint

# def get_prime_indexes(n):
#     return { sieve.search(k)[0] : v for k,v in factorint(n).items() }

# for i in range(1, 9):
#     print("{}: {}".format(i,
#         [get_prime_indexes(n) for n in get_numbers1(i)]
#     ))
