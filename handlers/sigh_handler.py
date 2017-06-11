from handler import Handler
from util import config
from managers.message_manager import send_message
from managers.config_manager import get_name
import util.constants as k

class Sigh(Handler):
    default_enabled = True
    name = 'sigh'
    triggers = (Handler.trigger_tag, [get_name()])
    response = '* sigh *'

    def __init__(self):
        Handler.__init__(self)

    def make_config(self):
        return config.make_config(self.default_enabled, [self.triggers])

    def process_message(self, slack_client, message):
        if self.is_triggered(message):
            send_message(slack_client, self.response, message[k.channel])