from handler import Handler
from util import config
from managers.message_manager import send_message, pm_user
from managers.config_manager import update_conf
import util.constants as k
import random
from util import regular_expressions

class CallResponse(Handler):
    default_enabled = True
    name = 'callresponse'
    calls = 'calls'
    help_msg = 'To add a call type a message with the following format (Caps are important)\n' \
               '"Call:<Your text here> Response:<Response Here>"\n' \
               'To remove a call, use the following format\n' \
               '"Remove:<Your text here> Response:<Response Here>"\n'
    added_msg = 'Response added'
    removed_msg = 'Response removed'
    no_response_msg = 'No matching response found'

    def __init__(self):
        Handler.__init__(self)

    def make_config(self):
        return config.make_config(Handler.get_default_config_args(self) + [(self.calls, dict())])

    def get_response(self, msg_text):
        response = ''
        for key, values in self.conf[self.calls].iteritems():
            if key in msg_text:
                response = response + random.choice(values) + '\n'
        return response

    def add_call_response(self, call, response, slack_client, user_id):
        if call in self.conf[self.calls]:
            if response not in self.conf[self.calls][call]:
                self.conf[self.calls][call].append(response)
        else:
            self.conf[self.calls][call] = [response]
        update_conf(self.name, self.conf)
        pm_user(slack_client, self.added_msg, user_id)

    def remove_call_response(self, call, response, slack_client, user_id):
        if call in self.conf[self.calls]:
            if response in self.conf[self.calls][call]:
                self.conf[self.calls][call].remove(response)
                if not len(self.conf[self.calls][call]):
                    self.conf[self.calls].pop(call)
            pm_user(slack_client, self.removed_msg, user_id)
            update_conf(self.name, self.conf)
        else:
            pm_user(slack_client, self.no_response_msg, user_id)

    def process_message(self, slack_client, message):
        if self.should_parse_message(slack_client, message):
            msg_text = message[k.text]
            user_id = message[k.user]

            call_response_match = regular_expressions.call_response.match(msg_text)
            if call_response_match:
                self.add_call_response(call_response_match.group(k.call),
                                       call_response_match.group(k.response), slack_client, user_id)
                return

            remove_response_match = regular_expressions.remove_response.match(msg_text)
            if remove_response_match:
                self.remove_call_response(remove_response_match.group(k.remove),
                                          remove_response_match.group(k.response), slack_client, user_id)
                return

            response = self.get_response(msg_text)
            if response:
                send_message(slack_client, response, message[k.channel])
