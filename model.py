import random

class User:
    def __init__(self):
        self.id = random.randint(0, 20)
        self.answers = {}

