import sys
import time

from slackclient import SlackClient

from handlers import revive_handler
from managers.handler_manager import HandlerManager
from util.file_IO import get_API_token
from util.logger import write_to_log, prune_logs

slack_client = SlackClient(get_API_token())

stay_alive = True
pokemon_mode = True

def run(slack_client):
    if slack_client.rtm_connect():

        revive_handler.revive(slack_client)
        handler_manager = HandlerManager()

        while handler_manager.should_stay_alive():
            for message in slack_client.rtm_read():

                handler_manager.process_message(slack_client, message)

            time.sleep(0.1)
        return handler_manager.should_stay_alive()
    return True


while stay_alive:
    if pokemon_mode:
        try:
            stay_alive = run(slack_client)
        except:
            # We are pokemon trainers here
            # Gotta catch em all
            write_to_log(sys.exc_info())
            prune_logs()
    else:
        stay_alive = run(slack_client)
