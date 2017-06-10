from handler import Handler
from util import config
from managers.message_manager import pm_user
from managers.config_manager import can_user_edit

class Enabled(Handler):
    default_enabled = True
    name = 'enabled'
    triggers = (Handler.trigger_tag, ['disable', 'enable'])
    responses = [' was disabled', ' was enabled']

    def __init__(self, get_config, update_config, is_handler):
        self.get_config = get_config
        self.update_config = update_config
        self.is_handler = is_handler
        Handler.__init__(self)

    def make_config(self):
        return config.make_config(self.default_enabled, [self.triggers])

    def is_message_in_format(self, message):
        words = message.split()
        return len(words) == 2 and \
            words[0] in self.conf[Handler.trigger_tag] and \
            self.is_handler(words[1])

    def should_trigger(self, message):
        if not self.conf[config.enabled]:
            return False
        if 'text' in message and 'user' in message:
            msg = message['text']
            return self.is_message_in_format(msg)
        return False

    def edit_handler(self, name, enabled=True):
        conf = self.get_config(name)
        if config.enabled in conf:
            conf[config.enabled] = enabled
        return self.update_config(name, conf)

    def get_info(self, message):
        words = message.split()
        return self.conf[Handler.trigger_tag][1] == words[0], words[1]

    def trigger(self, slack_client, message):

        user_id = message['user']
        if can_user_edit(user_id):
            enabled, name = self.get_info(message['text'])
            if self.edit_handler(name, enabled = enabled):
                message = name + self.responses[enabled]
            else:
                message = "Failed to edit " + name
        else:
            message = 'Insufficent permissions'
        pm_user(slack_client, message, user_id)