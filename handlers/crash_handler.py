from handler import Handler
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

    def process_message(self, slack_client, message):
        if self.should_parse_message(slack_client, message):
            msg_text = message[k.text]
            if self.is_named(msg_text):
                raise Exception('test')
