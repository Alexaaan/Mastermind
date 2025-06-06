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
def check(secret_code: str, guess: str):
    """
    Compare le guess au secret_code et retourne un tuple (black_pins, white_pins).
    Les deux chaînes sont de même longueur (4 chiffres).
    """
    black = sum(s == g for s, g in zip(secret_code, guess))
    white = 0
    # Comptage des chiffres restants à comparer pour les pions blancs
    secret_count = {}
    guess_count = {}
    for s, g in zip(secret_code, guess):
        if s != g:
            secret_count[s] = secret_count.get(s, 0) + 1
            guess_count[g] = guess_count.get(g, 0) + 1
    for num in guess_count:
        if num in secret_count:
            white += min(secret_count[num], guess_count[num])
    return black, white
