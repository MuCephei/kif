from handler import Handler
from util import config
from managers.message_manager import pm_user
from managers.config_manager import can_user_edit
import util.constants as k
from util.regular_expressions import two_words

class Config(Handler):
    default_enabled = True
    name = 'config'
    disabled_response = ' was disabled'
    enabled_response = ' was enabled'
    reset_response = ' was reset'
    failure_response = ' But nothing happened!'
    reset_tag = 'reset'
    enable_tag = 'enable'
    disable_tag = 'disable'

    def __init__(self, get_config, update_config, is_handler, reset_conf):
        self.get_config = get_config
        self.update_config = update_config
        self.is_handler = is_handler
        self.reset_conf = reset_conf
        Handler.__init__(self)

    def make_config(self):
        return config.make_config(self.default_enabled)

    def enable(self, name):
        if self.edit_enabled(name, True):
            return self.enabled_response
        return self.failure_response

    def disable(self, name):
        if self.edit_enabled(name, False):
            return self.disabled_response
        return self.failure_response

    def edit_enabled(self, name, enabled=True):
        conf = self.get_config(name)
        if config.enabled in conf:
            conf[config.enabled] = enabled
        return self.update_config(name, conf)

    def reset(self, name):
        if self.reset_conf(name):
            return self.reset_response
        return self.failure_response

    def process_message(self, slack_client, message):
        if not self.conf[config.enabled]:
            return
        if k.text not in message or k.user not in message:
            return
        user_id = message['user']
        if can_user_edit(user_id):
            msg_text = message[k.text].lower()
            regex_match = two_words.match(msg_text)
            if regex_match:
                command = regex_match.group(k.command)
                name = regex_match.group(k.name)
                if command == self.reset_tag:
                    fct = self.reset
                elif command == self.enable_tag:
                    fct = self.enable
                elif command == self.disable_tag:
                    fct = self.disable
                else:
                    return
                response = name + fct(name)
                pm_user(slack_client, response, user_id)

        # This is not a config editable handler
        # Which is slightly ironic, but would be a massive pain
