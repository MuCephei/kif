import util.api_calls as api
import config_manager
from channel_manager import get_channel_by_user_id

def send_message_as_self(slack_client, msg, channel):
    send_message(slack_client, msg, channel,
                 config_manager.get_name(),
                 config_manager.get_icon())

def send_message(slack_client, msg, channel, other=None, icon=':kif:'):
    if other:
        api.write_msg_as_other(slack_client, msg, channel, other, icon)
    else:
        api.write_msg_as_user(slack_client, msg, channel)

def pm_user(slack_client, msg, user_id):
    pm_channel = get_channel_by_user_id(user_id, slack_client)
    send_message(slack_client, msg, pm_channel)
