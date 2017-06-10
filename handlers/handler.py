from managers.config_manager import get_config
from util import config

class Handler:
    name = 'handler'
    trigger_tag = 'triggers'
    default_enabled = True

    def __init__(self):
        self.conf = get_config(self.name, fct = self.make_config)

    def make_config(self):
        return config.make_config(self.default_enabled)

    def should_trigger(self, message):
        if not self.conf[config.enabled]:
            return False
        if 'text' in message and 'user' in message:
            msg = message['text']
            for t in self.conf[Handler.trigger_tag]:
                if t in msg:
                    return True
        return False

    def trigger(self, slack_client, message):
        pass

    def reload(self):
        self.__init__()

