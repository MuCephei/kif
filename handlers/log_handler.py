from handlers.handler import Handler
from managers.config_manager import get_bot_name
from managers.message_manager import pm_user
import util.constants as k
from util import logger

class Log(Handler):
    default_enabled = True
    name = 'log'
    list_tag = 'list'
    item_tag = 'item'
    no_logs = 'No Error Logs'
    invalid_input = 'Invalid Input'

    def __init__(self):
        Handler.__init__(self)
        self.handler_commands = self.get_handler_commands()

    def get_handler_commands(self):
        #commands must take user id and slack_client as an arg
        return {self.list_tag: self.list_command,
                self.item_tag: self.item_command}

    def list_command(self, slack_client, user_id, arg='0'):
        try:
            arg = int(arg)
            logs = logger.get_log_list(arg)
            if logs:
                logs = [str(i) + ' ' + l for i, l in enumerate(logs)]
                pm_user(slack_client, '\n'.join(logs), user_id)
            else:
                pm_user(slack_client, self.no_logs, user_id)
        except:
            pm_user(slack_client, self.invalid_input, user_id)

    def item_command(self, slack_client, user_id, arg='0'):
        try:
            n = int(arg)
            msg = logger.get_log(n)
            pm_user(slack_client, msg, user_id)
        except:
            pm_user(slack_client, self.invalid_input, user_id)

    def get_help_msg(self):
        return 'This allows users to view and interact with error logs\n' + \
               'usage is <' + get_bot_name() + ' ' + self.name + '>'

    def process_message(self, slack_client, msg_text, user_id, channel, timestamp, args):
        if self.should_parse_message(slack_client, msg_text, user_id, channel):
            if self.is_handler_named(msg_text):
                self.item_command(slack_client, user_id)
            else:
                command = self.get_named_handler_command(msg_text)
                if command:
                    if command in self.handler_commands:
                        self.handler_commands[command](slack_client, user_id)
                    else:
                        self.item_command(slack_client, user_id, command)
                else:
                    command, arg = self.get_named_handler_command_with_arg(msg_text)
                    if command and command in self.handler_commands:
                        self.handler_commands[command](slack_client, user_id, arg)
