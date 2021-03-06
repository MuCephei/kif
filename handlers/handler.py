from managers.config_manager import get_config
from util import config
import util.constants as k
from util.regular_expressions import words
from managers.config_manager import get_bot_name, update_conf, can_user_edit
from managers.message_manager import pm_user

class Handler:
    name = 'handler'
    opt_out = 'opt_out'
    enabled = 'enabled'
    default_enabled = True
    insufficient_permission_msg = 'Insufficient Permissions'
    enabled_msg = 'Enabled '
    disabled_msg = 'Disabled '
    reset_msg = 'Reset '
    opt_out_msg = 'Opted out of '
    opt_in_msg = 'Opted in to '

    def __init__(self):
        self.conf = get_config(self.name, fct = self.make_config)
        self.commands = self.get_commands()

    def get_help_msg(self):
        return 'This is a default help message and should not be used'

    def get_commands(self):
        #commands must take user id and slack_client as an arg
        return {k.start: self.user_opt_in,
                    k.stop: self.user_opt_out,
                    k.reset: self.reset,
                    k.enable: self.enable,
                    k.disable: self.disable,
                    k.help: self.help}

    def get_default_config_args(self):
        return [(self.enabled, self.default_enabled), (self.opt_out, [])]

    def make_config(self):
        return config.make_config(self.get_default_config_args())

    @staticmethod
    def _is_bot_named(string):
        return get_bot_name() in string

    def _is_named_call(self, string):
        return self._is_bot_named(string) and self.name in string

    def is_handler_named(self, string):
        match = words[2].match(string)
        return match and match.group(k.first) == get_bot_name() and match.group(k.second) == self.name

    def get_named_handler_command(self, string):
        match = words[3].match(string)
        if match and match.group(k.first) == get_bot_name() and match.group(k.second) == self.name:
            return match.group(k.third)
        return False

    def get_named_handler_command_with_arg(self, string):
        match = words[4].match(string)
        if match and match.group(k.first) == get_bot_name() and match.group(k.second) == self.name:
            return match.group(k.third), match.group(k.fourth)
        return False, False

    def enable(self, user_id, slack_client):
        if can_user_edit(user_id):
            if self.enabled in self.conf:
                self.conf[self.enabled] = True
                update_conf(self.name, self.conf)
                pm_user(slack_client, self.enabled_msg + self.name, user_id)
        else:
            pm_user(slack_client, self.insufficient_permission_msg + self.name, user_id)

    def disable(self, user_id, slack_client):
        if can_user_edit(user_id):
            if self.enabled in self.conf:
                self.conf[self.enabled] = False
                update_conf(self.name, self.conf)
                pm_user(slack_client, self.disabled_msg + self.name, user_id)
        else:
            pm_user(slack_client, self.insufficient_permission_msg + self.name, user_id)

    def reset(self, user_id, slack_client):
        if can_user_edit(user_id):
            self.conf = self.make_config()
            update_conf(self.name, self.conf)
            pm_user(slack_client, self.reset_msg + self.name, user_id)
        else:
            pm_user(slack_client, self.insufficient_permission_msg + self.name, user_id)

    def help(self, user_id, slack_client):
        pm_user(slack_client, self.get_help_msg(), user_id)

    def user_opt_out(self, user_id, slack_client):
        if user_id not in self.conf[self.opt_out]:
            self.conf[self.opt_out].append(user_id)
            update_conf(self.name, self.conf)
            pm_user(slack_client, self.opt_out_msg + self.name, user_id)

    def user_opt_in(self, user_id, slack_client):
        if user_id in self.conf[self.opt_out]:
            self.conf[self.opt_out].remove(user_id)
            update_conf(self.name, self.conf)
            pm_user(slack_client, self.opt_in_msg + self.name, user_id)

    def get_named_command(self, msg_text):
        regex_match = words[2].match(msg_text)
        if regex_match and regex_match.group(k.second) == self.name:
            return regex_match.group(k.first)
        return False

    def should_parse_message(self, slack_client, msg_text, user_id, channel):
        # The check to see if kif sent it happens higher up
        if not msg_text or not user_id or not channel:
            return False

        command = self.get_named_command(msg_text)
        if command and command in self.commands:
            fct = self.commands[command]
            fct(user_id, slack_client)

        if not self.conf[self.enabled]:
            return False

        return user_id not in self.conf[self.opt_out]
