from typing import Tuple, List
from collections import Counter
from random import choice


def bullcows(guess: str, ground_truth: str) -> Tuple[int, int]:

    bulls = 0
    cows = 0
    for ch_guess, ch_gt in zip(guess, ground_truth):
        bulls += ch_guess == ch_gt
    guess_letters = Counter(guess)
    gt_letters = Counter(ground_truth)
    intersecting_letters = set(
        list(guess_letters.keys()) + list(gt_letters.keys()))

    for lt in intersecting_letters:
        cows += min(guess_letters[lt], gt_letters[lt])
    cows -= bulls

    return bulls, cows


def ask(prompt: str, valid: List[str] = None) -> str:

    print(prompt)
    guess = input()
    if (valid is not None) and (guess != valid):
        print(prompt)
        guess = input()

    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string, bulls, cows)


def game
