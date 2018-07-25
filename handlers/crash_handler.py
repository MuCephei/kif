from handlers.handler import Handler
from managers.config_manager import get_bot_name
import util.constants as k

class Crash(Handler):
    default_enabled = True
    name = 'crash'

    def __init__(self):
        Handler.__init__(self)

    def get_help_msg(self):
        return 'This raises an exception to test error handling and logging\n' + \
        'usage is <' + get_bot_name() + ' ' + self.name + '>'

    def process_message(self, slack_client, msg_text, user_id, channel, timestamp, args):
        if self.should_parse_message(slack_client, msg_text, user_id, channel):
            if self.is_handler_named(msg_text):
                raise Exception('test')
            elif self._is_named_call(msg_text):
                raise Exception(msg_text)
