import numpy as np

def roll(number, dice, modifier, show):
    #returns the string and the value
    base = 1
    if dice == 1:
        base = 0
    if show:
        rolls = np.random.randint(base, dice, number)
        result = sum(rolls) + modifier
        return ','.join(map(str, rolls)) + ' + ' + str(modifier) + ' = ' + str(result), result
    else:
        roll = sum(np.random.randint(base, dice, number)) + modifier
        return str(roll), roll

def roll_advantage(number, dice, modifier, show):
    return max(roll(number, dice, modifier, show), roll(number, dice, modifier, show), key=lambda r: r[1])

def roll_disadvantage(number, dice, modifier, show):
    return min(roll(number, dice, modifier, show), roll(number, dice, modifier, show), key=lambda r: r[1])