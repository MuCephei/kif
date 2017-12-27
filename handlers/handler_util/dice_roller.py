import numpy as np

def roll(number, dice, modifier, show, best, worst, great):
    return _roll(number, dice, modifier, show, best, worst, great)[0]

def _roll(number, dice, modifier, show, best, worst, great):
    #returns the string and the value
    base = 1
    if dice == 1:
        base = 0

    rolls = np.random.randint(base, dice, number)
    rolls = map(lambda r: r if r > great else np.random.randint(base, dice), rolls)
    result = sum(rolls) + modifier
    bold_numbers = set()
    if best:
        sorted_rolls = sorted(rolls, reverse = True)
        result = sum(sorted_rolls[:best]) + modifier
        bold_numbers = set(list(reversed(np.argsort(rolls)))[:best])
    elif worst:
        sorted_rolls = sorted(rolls, reverse = False)
        result = sum(sorted_rolls[:worst]) + modifier
        bold_numbers = set(np.argsort(rolls)[:worst])

    if show:
        left = ','.join(map(lambda i: '*' + str(rolls[i]) + '*' if i in bold_numbers else str(rolls[i]), range(len(rolls))))
        return left + ' + ' + str(modifier) + ' = ' + str(result), result
    else:
        return str(result), result


def roll_advantage(number, dice, modifier, show, best, worst, great):
    adv = max(_roll(number, dice, modifier, show, best, worst, great),
              _roll(number, dice, modifier, show, best, worst, great), key=lambda r: r[1])
    return adv[0] + ' (advantage)'


def roll_disadvantage(number, dice, modifier, show, best, worst, great):
    dis = min(_roll(number, dice, modifier, show, best, worst, great),
              _roll(number, dice, modifier, show, best, worst, great), key=lambda r: r[1])
    return dis[0] + ' (disadvantage)'
