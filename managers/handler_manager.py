from handlers import call_response_handler, id_handler, sigh_handler, crash_handler
from user_manager import get_my_id
import util.constants as k

class HandlerManager:

    def __init__(self):
        self.handlers = [sigh_handler.Sigh(),
                         id_handler.Id(),
                         call_response_handler.CallResponse(),
                         crash_handler.Crash()]

    def process_message(self, slack_client, message):
        if k.user in message and message[k.user] != get_my_id(slack_client):
            for h in self.handlers:
                h.process_message(slack_client, message)
