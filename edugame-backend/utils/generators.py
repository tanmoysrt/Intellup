import string
import random

def randomStringGenerator(length=10):
    res = ''.join(random.choices((string.ascii_uppercase + string.digits),k = length))
    return res


# print(random.sample(range(1, 6), 5))

def generate_random_filename(filename):
    extension = str(filename).split(".")[-1]
    random_name = str(random.randint(1111111111111111,9999999999999999))
    final_random_name = random_name+"."+extension
    return final_random_name