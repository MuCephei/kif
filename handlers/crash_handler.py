from handler import Handler
from util import config
from util import regular_expressions
from managers.config_manager import get_name
import util.constants as k

class Crash(Handler):
    default_enabled = True
    name = 'crash'

    def __init__(self):
        Handler.__init__(self)

    def make_config(self):
        return config.make_config(self.default_enabled)

    def process_message(self, slack_client, message):
        if not self.conf[config.enabled]:
            return
        if k.text not in message or k.user not in message or k.channel not in message:
            return
        msg_text = message[k.text]
        regex_match = regular_expressions.two_words.match(msg_text)
        if regex_match and regex_match.group(k.name) == get_name() and regex_match.group(k.command) == 'crash':
            raise Exception('test')
