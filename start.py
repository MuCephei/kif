import time
from slackclient import SlackClient
from managers import revive_manager
from managers.handler_manager import HandlerManager
from util.file_IO import get_API_token
from util.logger import write_to_log
import util.constants as k
import sys

slack_client = SlackClient(get_API_token())

stay_alive = True
pokemon_mode = True

def run(slack_client):
    stay_alive = True
    if slack_client.rtm_connect():

        revive_manager.revive(slack_client)
        handler_manager = HandlerManager()

        while stay_alive:
            for message in slack_client.rtm_read():

                msg_text = '' if k.text not in message else message[k.text]
                user_id = '' if k.user not in message else message[k.user]
                channel = '' if k.channel not in message else message[k.channel]

                handler_manager.process_message(slack_client, msg_text, user_id, channel)

                stay_alive = revive_manager.process_message(slack_client, msg_text, user_id, channel)

            time.sleep(0.1)
    return stay_alive

while stay_alive:
    if pokemon_mode:
        try:
            stay_alive = run(slack_client)
        except:
            # We are pokemon trainers here
            # Gotta catch em all
            write_to_log(sys.exc_info())
    else:
        stay_alive = run(slack_client)
