import string
import random


password_chars = list(string.digits + string.ascii_lowercase)
usernames_chars = list(string.ascii_uppercase)

random.shuffle(password_chars)
random.shuffle(usernames_chars)


def random_string(characters=None, size=5):
    # Creates random string with certain size from characters.
    if characters is None:
        characters = string.printable
    characters = list(characters[:size])
    random.shuffle(characters)
    return "".join(characters)

def random_username(size=5):
    # Creates radom username from uppercase characters.
    return random_string(usernames_chars, size)

def random_password(size=5):
    # Creates radom username from uppercase and digits characters.
    return random_string(password_chars, size)

def generate_total(first_total, second_total):
    # Returns difference of arguments else 0 if second is larger than first.
    total_ = first_total - second_total
    if total_ < 0:
        total_ = 0
    return total_


def shuffle_iterables(*iterables):
    # Shuffles iterables by first combining their shuffled items.
    combined = []
    for iterable in iterables:
        combined.extend(iterable)
    random.shuffle(combined)
    return combined

def random_strings(total, characters=None, strings=[], size=5):
    # Creates random strings containing 'strings' argument items.
    gen_total = generate_total(total, len(strings))
    gen_strings = [random_string(size) for _ in range(gen_total)]
    return shuffle_iterables(gen_strings, strings)


def random_usernames(total, usernames=[], size=5):
    # Creates random usernames usernames
    gen_total = generate_total(total, len(usernames))
    gen_usernames = [random_username(size) for _ in range(gen_total)]
    return shuffle_iterables(gen_usernames, usernames)

def random_passwords(total, passwords=[], size=5):
    # Creates random passwords containing 'passwords' argument items.
    gen_total = generate_total(total, len(passwords))
    gen_passwords = [random_password(size) for _ in range(gen_total)]
    return shuffle_iterables(gen_passwords, passwords)


if __name__ == "__main__":
    print(random_passwords(4, ["john"]))