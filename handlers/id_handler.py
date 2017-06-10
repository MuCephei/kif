from handler import Handler
from util import config
from managers.message_manager import pm_user

class Id(Handler):
    default_enabled = True
    name = 'id'
    triggers = (Handler.trigger_tag, ['myid'])

    def __init__(self):
        Handler.__init__(self)

    def make_config(self):
        return config.make_config(self.default_enabled, [self.triggers])

    def trigger(self, slack_client, message):
        user_id = message['user']
        pm_user(slack_client, user_id, user_id)