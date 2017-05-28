import time
import subprocess
from slackclient import SlackClient

def get_API_token():
    with open('APIToken', 'r') as f:
        return f.readline().strip()

slack_client = SlackClient(get_API_token())

if slack_client.rtm_connect():
    stay_alive = True
    while stay_alive:
        for message in slack_client.rtm_read():
            if 'text' in message and 'kif' in message['text']:

                message_text = '* sigh *'

                slack_client.api_call(
                    "chat.postMessage",
                    channel=message['channel'],
                    text=message_text,
                    as_user=True)
            if 'text' in message and 'kif restart' in message['text']:
                message_text = 'restarting'

                slack_client.api_call(
                    "chat.postMessage",
                    channel=message['channel'],
                    text=message_text,
                    as_user=True)

                subprocess.call("~/restart_kif.sh")

                stay_alive = False

        time.sleep(1)

print("goodnight")

