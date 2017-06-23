from handlers import call_response_handler, id_handler, sigh_handler, crash_handler
from user_manager import get_my_id
from config_manager import get_bot_name
from message_manager import pm_user
from util.regular_expressions import two_words
import util.constants as k

class HandlerManager:

    def __init__(self):
        self.handlers = [sigh_handler.Sigh(),
                         id_handler.Id(),
                         call_response_handler.CallResponse(),
                         crash_handler.Crash()]

    def is_help_message(self, msg_text):
        match = two_words.match(msg_text)
        return match and match.group(k.first) == get_bot_name() and match.group(k.second) == k.help

    def help(self, slack_client, user_id):
        msg = 'For information about specific functions use the following command format' + \
            ' "help <handler>"\nTo opt out of a handler use "stop <handler>"\n' + \
            'To opt back in use "start <handler>"\nThe handlers are as follows:\n' + \
            '\n'.join(map(lambda h: '*' + h.name + '*', self.handlers))
        pm_user(slack_client, msg, user_id)

    def process_message(self, slack_client, message):
        if k.user in message:
            user = message[k.user]
            if user != get_my_id(slack_client):
                if k.text in message and self.is_help_message(message[k.text]):
                    self.help(slack_client, user)
                for h in self.handlers:
                    h.process_message(slack_client, message)
