from handler import Handler
from managers.message_manager import send_message
from managers.config_manager import get_bot_name
import util.constants as k

class Sigh(Handler):
    default_enabled = True
    name = 'sigh'
    response = '* sigh *'

    def __init__(self):
        Handler.__init__(self)

    def get_help_msg(self):
        return self.response

    def process_message(self, slack_client, message):
        if self.should_parse_message(slack_client, message):
            msg_text = message[k.text]
            if get_bot_name() in msg_text:
                send_message(slack_client, self.response, message[k.channel])
