def cache(fn):
    answers = {}

    def fn_cache(*args):
        if args not in answers:
            answers[args] = fn(*args)
        return answers[args]

    return fn_cache

def highest_first_step(width, n):
    return ((2 * n)//width - width + 1)/2

@cache
def solve_fixed_width(width, n):
    if width == 1:
        return 1

    ret = 0
    for first_step in range(1, highest_first_step(width, n) + 1):
        ret += solve_fixed_width(width - 1, n - (width * first_step))

    return ret

def answer(n):
    ret = 0
    width = 2

    while(highest_first_step(width, n) > 0):
        ret += solve_fixed_width(width, n)
        width += 1

    return ret

print(answer(200))