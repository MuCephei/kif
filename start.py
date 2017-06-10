import time
import subprocess
from slackclient import SlackClient
from managers import message_manager, channel_manager, user_manager
from managers.handler_manager import HandlerManager
from util.file_IO import read_file, write_to_file
from handlers import sigh_handler, id_handler

revive = 'revive'
api_token = 'APIToken'

def get_API_token():
    return read_file(api_token).strip()

def write_revive_msg(msg="I'm alive"):
    write_to_file(revive, msg)

def get_revive_msg():
    return read_file(revive).strip()

slack_client = SlackClient(get_API_token())

if slack_client.rtm_connect():

    revive_msg = get_revive_msg()
    killers_name = revive_msg.split()[0]
    killers_id = user_manager.get_user_by_name(killers_name)

    message_manager.send_message_as_self(slack_client, get_revive_msg(), killers_id)

    stay_alive = True

    handler_manager = HandlerManager()

    while stay_alive:
        for message in slack_client.rtm_read():

            handler_manager.process_message(slack_client, message)

            if 'text' in message and 'kif restart' in message['text']:
                message_text = 'restarting'

                channel_manager.update_channels(slack_client)
                message_manager.send_message_as_self(slack_client, message_text, message['channel'])

                name = user_manager.get_user_by_id(message['user'])
                write_revive_msg(msg = name + ' killed me')

                subprocess.call("/home/kif-bot/restart_kif.sh")

                stay_alive = False

        time.sleep(0.1)

