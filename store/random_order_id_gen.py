import random, string

def random_id_generator(length):
    letters = string.digits + string.ascii_letters
    return "".join(random.choice(letters) for i in range(length))