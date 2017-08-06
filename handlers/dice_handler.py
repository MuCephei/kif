from handler import Handler
from managers.message_manager import send_message
from util.regular_expressions import dice
from handler_util import dice_roller
import util.constants as k

class Dice(Handler):
    default_enabled = True
    name = 'dice'
    invalid_modifier = 'Invalid command'
    help_msg = 'To roll dice enter in the "ndm +/- q" format\n' + \
        'Where n is the number of dice, m is the number of sides and q is a modifier'

    def __init__(self):
        Handler.__init__(self)

    def get_help_msg(self):
        return self.help_msg

    def process_message(self, slack_client, msg_text, user_id, channel, timestamp, args):
        if self.should_parse_message(slack_client, msg_text, user_id, channel):
            match = dice.match(msg_text)
            if match:
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
                show = 'show' in args or 's' in args
                if 'advantage' in args or 'a' in args:
                    roll = dice_roller.roll_advantage(number, dice_type, modifier, show)[0]
                    roll += ' (advantage)'
                elif 'disadvantage' in args or 'd' in args:
                    roll = dice_roller.roll_disadvantage(number, dice_type, modifier, show)[0]
                    roll += ' (disadvantage)'
                else:
                    roll = dice_roller.roll(number, dice_type, modifier, show)[0]
                send_message(slack_client, roll, channel)

