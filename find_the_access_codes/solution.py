from math import factorial
from collections import Counter

def combination(n, r):
    if n < r:
        return 0
    return reduce(lambda x,y: x*y, range(n - r + 1, n + 1)) / factorial(r)

def answer(l):
    ret = 0
    limit = l[-1]
    c = Counter(l)

    for n1 in c:
        for n2 in range(n1, limit + 1, n1):
            if n2 not in c:
                continue

            for n3 in range(n2, limit + 1, n2):
                if n3 not in c:
                    continue

                c1 = c[n1]
                c2 = c[n2]
                c3 = c[n3]

                # If any values are equal, must perform nCr operation to
                # calculate number of different combinations available.
                if n1 == n2:
                    if n1 == n3:
                        ret += combination(c1, 3)
                    else:
                        ret += combination(c1, 2) * c3
                elif n2 == n3:
                    ret += combination(c2, 2) * c1
                else:
                    ret += c1 * c2 * c3
    return ret