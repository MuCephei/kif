import numpy as np

def roll(number, dice, modifier):
    return sum(np.random.randint(1, dice, number)) + modifier