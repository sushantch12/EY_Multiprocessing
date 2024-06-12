from multiprocessing import Pool

def add_two_numbers(pair):
    return sum(pair)

def perform_addition(payload):
    with Pool() as pool:
        result = pool.map(add_two_numbers, payload)
    return result
