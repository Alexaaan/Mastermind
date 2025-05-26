import random

COLORS = ['R', 'G', 'B', 'Y', 'O', 'P']

def generate_code(length=4):
    return [random.choice(COLORS) for _ in range(length)]

def check_guess(secret, guess):
    well = sum(s == g for s, g in zip(secret, guess))
    sc, gc = {}, {}
    for s, g in zip(secret, guess):
        if s != g:
            sc[s] = sc.get(s, 0) + 1
            gc[g] = gc.get(g, 0) + 1
    misplaced = sum(min(gc[c], sc.get(c, 0)) for c in gc)
    return { 'well_placed': well, 'misplaced': misplaced }
