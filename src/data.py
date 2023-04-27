import random

def generate_random_array(min_value, max_value, length):
    return random.sample(range(min_value, max_value), length)