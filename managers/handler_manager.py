from handlers import *
from config_manager import get_bot_name
from message_manager import pm_user
from util.regular_expressions import words
from user_manager import get_my_id
import util.constants as k

class HandlerManager:

    def __init__(self):
        self.alive = True
        self.handlers = [sigh_handler.Sigh(),
                         id_handler.Id(),
                         call_response_handler.CallResponse(self),
                         crash_handler.Crash(),
                         log_handler.Log(),
                         dice_handler.Dice()
                         ]

    def is_help_message(self, msg_text):
        match = words[2].match(msg_text)
        return match and match.group(k.first) == get_bot_name() and match.group(k.second) == k.help

    def help(self, slack_client, user_id):
        msg = 'For information about specific functions use the following command format' + \
            ' "help <handler>"\nTo opt out of a handler use "stop <handler>"\n' + \
            'To opt back in use "start <handler>"\nThe handlers are as follows:\n' + \
            '\n'.join(map(lambda h: '*' + h.name + '*', self.handlers))
        pm_user(slack_client, msg, user_id)

    def should_stay_alive(self):
            return self.alive

    def process_message(self, slack_client, message=None, input_text='', user_id='', channel='', timestamp='', args=[]):

        if message:
            input_text = '' if k.text not in message else message[k.text]
            user_id = '' if k.user not in message else message[k.user]
            channel = '' if k.channel not in message else message[k.channel]
            timestamp = '' if k.timestamp not in message else message[k.timestamp]

        sections = input_text.split(' --')
        msg_text = sections[0]
        args += sections[1:]

        if user_id:
            if user_id != get_my_id(slack_client):
                if msg_text and self.is_help_message(msg_text):
                    self.help(slack_client, user_id)
                for h in self.handlers:
                    h.process_message(slack_client, msg_text, user_id, channel, timestamp, args)

                self.alive = revive_handler.process_message(slack_client, msg_text, user_id, channel, timestamp, args)
