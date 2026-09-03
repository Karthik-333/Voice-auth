import random
import re


WORDS_1 = [
    "blue",
    "red",
    "green",
    "silver",
    "golden",
    "purple"
]

WORDS_2 = [
    "tiger",
    "elephant",
    "falcon",
    "dragon",
    "lion",
    "wolf"
]


def generate_challenge():
    word1 = random.choice(WORDS_1)
    word2 = random.choice(WORDS_2)
    number = random.randint(10, 99)

    return f"{word1} {word2} {number}"


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = " ".join(text.split())

    return text


def verify_challenge(expected, received):
    expected_normalized = normalize_text(expected)
    received_normalized = normalize_text(received)

    return expected_normalized == received_normalized
