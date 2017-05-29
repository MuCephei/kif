import time
import subprocess
import SlackClientWrapper

slack_client = SlackClientWrapper()

if slack_client.connect():

    slack_client.send_message("I'm alive", "#zac-testing")

    stay_alive = True
    while stay_alive:
        for message in slack_client.get_messages():
            if 'text' in message and 'kif' in message['text']:

                message_text = '* sigh *'

                slack_client.send_message(message_test, message['channel'])

            if 'text' in message and 'kif restart' in message['text']:
                message_text = 'restarting'

                slack_client.send_message(message_text, message['channel'])

                subprocess.call("~/restart_kif.sh")

                stay_alive = False

        time.sleep(0.1)

