from slackclient import SlackClient

class SlackClientWrapper(Object):
    API_TOKEN_FILE = 'APIToken'

    def __init__(self):
        self.slack_client = SlackClient(__get_API_token())

    def connect(self):
        return self.slack_client.rtm_connect()

    def get_messages(self):
        return self.slack_client.rtm_read()

    def send_message(self, message, channel, show_typing = False):
        if(show_typing):
            self.slack_client.send_user_typing_pause(channel)

        slack_client.api_call(
            "chat.postMessage",
            channel = channel,
            text = message,
            as_user=True)

    def __get_API_token():
        with open(API_TOKEN_FILE, 'r') as f:
            return f.readline().strip()
