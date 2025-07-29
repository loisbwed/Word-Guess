import random

def init_game(word_file='words.txt'):
    word_bank = []
    try:
        with open(word_file) as f:
            for line in f:
                if len(line.strip()) == 5:
                    word_bank.append(line.strip().lower())
    except FileNotFoundError:
        return None
    except Exception as e:
        return None
    return random.choice(word_bank) if word_bank else None


def check_guess(guess, word_to_guess):
    correct_letters = []
    misplaced_letters = []
    incorrect_letters = []

    for i, letter in enumerate(guess):
        if letter == word_to_guess[i]:
            correct_letters.append(letter)
        elif letter in word_to_guess:
            misplaced_letters.append(letter)
        else:
            incorrect_letters.append(letter)

    return correct_letters, misplaced_letters, incorrect_letters