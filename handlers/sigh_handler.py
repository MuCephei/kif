from handler import Handler
from util.api_calls import write_msg
import config

class Sigh(Handler):
    default_enabled = True
    name = 'sigh'
    triggers = ('triggers', ['kif'])
    response = '* sigh *'

    def __init__(self):
        Handler.__init__(self)

    def make_config(self):
        return config.make_config(self.default_enabled, [self.triggers])

    def should_trigger(self, message):
        triggered = False
        if 'text' in message:
            msg = message['text']
            for t in self.conf[self.triggers[0]]:
                if t in msg:
                    triggered = True
        return self.conf[config.enabled] and triggered

    def trigger(self, slack_client, message):
        write_msg(slack_client, self.response, message['channel'])