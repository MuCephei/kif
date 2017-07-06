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
    words_calls = 'word_calls'
    help_msg = 'To add a call type a message with the following format (Caps are important)\n' \
               'Your text here>>>Response Here\n' \
               'To remove a call, use the following format\n' \
               'Your text here<<<Response Here\n'
    added_msg = 'Response added'
    removed_msg = 'Response removed'
    no_response_msg = 'No matching response found'

    def __init__(self):
        Handler.__init__(self)

    def get_help_msg(self):
        return self.help_msg

    def make_config(self):
        return config.make_config(Handler.get_default_config_args(self)
                                  + [(self.calls, dict()), (self.words_calls, dict())])

    def get_response(self, msg_text):
        response = ''
        for key, values in self.conf[self.calls].iteritems():
            if key in msg_text:
                response = response + random.choice(values) + '\n'

        words = msg_text.split()
        for key, values in self.conf[self.words_calls].iteritems():
            if key in words:
                response = response + random.choice(values) + '\n'

        return response

    def add_call_response(self, call, response, slack_client, user_id, type=None):
        if not type:
            type = self.calls
        if call in self.conf[type]:
            if response not in self.conf[type][call]:
                self.conf[type][call].append(response)
        else:
            self.conf[type][call] = [response]
        update_conf(self.name, self.conf)
        pm_user(slack_client, self.added_msg, user_id)

    def remove_call_response(self, call, response, slack_client, user_id, type=None):
        if not type:
            type = self.calls
        if call in self.conf[type]:
            if response in self.conf[type][call]:
                self.conf[type][call].remove(response)
                if not len(self.conf[type][call]):
                    self.conf[type].pop(call)
            pm_user(slack_client, self.removed_msg, user_id)
            update_conf(self.name, self.conf)
        else:
            pm_user(slack_client, self.no_response_msg, user_id)

    def call_response(self, slack_client, user_id, msg_text):
        match = regular_expressions.call_response.match(msg_text)
        if match:
            self.add_call_response(match.group(k.call),
                                   match.group(k.response), slack_client, user_id, type=self.calls)
            return True
        return False

    def remove_response(self, slack_client, user_id, msg_text):
        match = regular_expressions.remove_response.match(msg_text)
        if match:
            self.remove_call_response(match.group(k.call),
                                      match.group(k.response), slack_client, user_id, type=self.calls)
            return

    def word_call_response(self, slack_client, user_id, msg_text):
        match = regular_expressions.word_call_response.match(msg_text)
        if match:
            self.add_call_response(match.group(k.call),
                                   match.group(k.response), slack_client, user_id, type=self.words_calls)
            return True
        return False

    def word_remove_response(self, slack_client, user_id, msg_text):
        match = regular_expressions.word_remove_response.match(msg_text)
        if match:
            self.remove_call_response(match.group(k.call),
                                      match.group(k.response), slack_client, user_id, type=self.words_calls)
            return

    def process_message(self, slack_client, message):
        if self.should_parse_message(slack_client, message):
            msg_text = message[k.text].strip()
            user_id = message[k.user]

            if self.word_remove_response(slack_client, user_id, msg_text):
                return
            elif self.word_call_response(slack_client, user_id, msg_text):
                return
            elif self.call_response(slack_client, user_id, msg_text):
                return
            elif self.remove_response(slack_client, user_id, msg_text):
                return

            response = self.get_response(msg_text)
            if response:
                send_message(slack_client, response, message[k.channel])
