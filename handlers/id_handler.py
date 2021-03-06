from handlers.handler import Handler
from managers.message_manager import pm_user
from managers.config_manager import get_bot_name

class Id(Handler):
    default_enabled = True
    name = 'id'

    def __init__(self):
        Handler.__init__(self)

    def get_help_msg(self):
        return 'This direct messages you your user id\n' + \
        'usage is <' + get_bot_name() + ' ' + self.name + '>'

    def process_message(self, slack_client, msg_text, user_id, channel, timestamp, args):
        if self.should_parse_message(slack_client, msg_text, user_id, channel):
            if self.is_handler_named(msg_text):
                pm_user(slack_client, user_id, user_id)
