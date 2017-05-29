import time
import subprocess
from slackclient import SlackClient

def get_API_token():
    with open('APIToken', 'r') as f:
        return f.readline().strip()

def write_revive_msg(msg="I'm alive"):
    with open('revive', 'w') as f:
        f.write(msg)

def get_revive_msg():
    with open('revive', 'r') as f:
        f.readline().strip()

slack_client = SlackClient(get_API_token())

if slack_client.rtm_connect():

    slack_client.api_call(
        "chat.postMessage",
        channel='#zac-testing',
        text=get_revive_msg(),
        as_user=True)

    write_revive_msg()

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

                write_revive_msg(message['user'] + " killed me")

                subprocess.call("/home/kif-bot/restart_kif.sh")

                stay_alive = False

        time.sleep(0.1)

