from typing import Tuple, List, Optional
from collections import Counter
import sys
import os
from random import choice
from urllib.request import urlopen


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
    if (valid is not None):
        while (not (guess in valid)):
            print(prompt)
            guess = input()

    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def gameplay(ask: callable, inform: callable, words: List[str]) -> int:
    gt_word = choice(words)
    attempts = 0
    bulls, cows = -1, 0
    while bulls != len(gt_word):
        attempts += 1
        guess = ask('Введите слово: ', words)
        bulls, cows = bullcows(guess, gt_word)
        inform("Быки: {}, Коровы: {}", bulls, cows)
    print(attempts)


if __name__ == '__main__':
    words_path, length = sys.argv[1], int(sys.argv[2])
    words = ''
    if os.path.isfile(words_path):
        with open(words_path) as f:
            words = f.readlines()
        words = [word.strip() for word in words]
    else:
        data = urlopen(words_path)
        encoding = data.headers.get_param('charset')
        if encoding is not None:
            words = data.read().decode(encoding).split()
        else:
            words = data.read().decode('utf-8').split()
    words = [word for word in words if len(word) == length]
    gameplay(ask, inform, words)
