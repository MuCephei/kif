from handler import Handler
from managers.message_manager import send_message
from util.regular_expressions import dice
from handler_util import dice_roller
import util.constants as k

class Dice(Handler):
    default_enabled = True
    name = 'dice'
    invalid_modifier = 'Invalid command'
    cannot_be_best_and_worst = 'Cannot roll with both the best and the worst'
    help_msg = 'To roll dice enter in the "ndm +/- q" format\n' + \
        'Where n is the number of dice, m is the number of sides and q is a modifier'

    def __init__(self):
        Handler.__init__(self)

    def get_help_msg(self):
        return self.help_msg

    def process_message(self, slack_client, msg_text, user_id, channel, timestamp, args):
        if self.should_parse_message(slack_client, msg_text, user_id, channel):
            for match in dice.finditer(msg_text):
                number = int(match.group(k.number_dice))
                dice_type = int(match.group(k.dice_type)) + 1
                sign = match.group(k.dice_sign)
                modifier = match.group(k.dice_modifier)
                if sign and len(sign) > 1:
                    send_message(slack_client, Dice.invalid_modifier, channel)
                    return
                elif sign and modifier:
                    modifier = (-1 if sign == '-' else 1) * int(modifier)
                else:
                    modifier = 0
                show = k.show in args or k.short_ in args
                best = int(args[k.best]) if k.best in args and args[k.best] else 0
                worst = int(args[k.worst]) if k.worst in args and args[k.worst] else 0
                great = int(args[k.great]) if k.great in args and args[k.great] else 0
                if best and worst:
                    send_message(slack_client, self.cannot_be_best_and_worst, channel)
                else:
                    if k.advantage in args or k.advantage_ in args:
                        roll = dice_roller.roll_advantage(number, dice_type, modifier, show, best, worst, great)
                    elif k.disadvantage in args or k.disadvantage_ in args:
                        roll = dice_roller.roll_disadvantage(number, dice_type, modifier, show, best, worst, great)
                    else:
                        roll = dice_roller.roll(number, dice_type, modifier, show, best, worst, great)
                    send_message(slack_client, roll, channel)

