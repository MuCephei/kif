from handlers.handler import Handler
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
    alias_calls = 'alias_calls'
    help_msg = 'To add a call type a message with the following format (Caps are important)\n' \
               'Your text here>>>Response Here\n' \
               'To remove a call, use the following format\n' \
               'Your text here<<<Response Here\n'
    added_msg = 'Response added'
    removed_msg = 'Response removed'
    added_alias = 'Alias added'
    removed_alias = 'Alias removed'
    no_response_msg = 'No matching response found'

    def __init__(self, master_handler):
        Handler.__init__(self)
        self.master_handler = master_handler

    def get_help_msg(self):
        return self.help_msg

    def make_config(self):
        return config.make_config(Handler.get_default_config_args(self))

    def get_response(self, slack_client, msg_text, user_id, channel, timestamp, args):
        response = ''
        if self.calls in self.conf:
            for key, values in self.conf[self.calls].iteritems():
                if key in msg_text:
                    response += random.choice(values) + '\n'

        if self.words_calls in self.conf:
            words = msg_text.split()
            for key, values in self.conf[self.words_calls].iteritems():
                if key in words:
                    response += random.choice(values) + '\n'

        if self.alias_calls in self.conf:
            for key, value in self.conf[self.alias_calls].iteritems():
                if key in msg_text + user_id:
                    text = value[0]
                    args.update(value[1])
                    self.master_handler.process_message(slack_client,
                        input_text=text, user_id=user_id, channel=channel, timestamp=timestamp, args=args)

        return response

    def add_call_response(self, call, response, slack_client, user_id, type=None):
        if not type:
            type = self.calls
        if type not in self.conf:
            self.conf[type] = {}
        if call in self.conf[type]:
            if response not in self.conf[type][call]:
                self.conf[type][call].append(response)
        else:
            self.conf[type][call] = [response]
        update_conf(self.name, self.conf)
        pm_user(slack_client, self.added_msg, user_id)

    def add_alias(self, call, response, slack_client, user_id, args):
        if self.alias_calls not in self.conf:
            self.conf[self.alias_calls] = {}
        self.conf[self.alias_calls][call + user_id] = [response, args]
        update_conf(self.name, self.conf)
        pm_user(slack_client, self.added_alias, user_id)


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

    def remove_alias(self, call, slack_client, user_id):
        if self.alias_calls not in self.conf:
            self.conf[self.alias_calls] = {}
        del self.conf[self.alias_calls][call + user_id]
        update_conf(self.name, self.conf)
        pm_user(slack_client, self.removed_alias, user_id)

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

    def alias_call_response(self, slack_client, user_id, msg_text, args):
        match = regular_expressions.alias_call_response.match(msg_text)
        if match:
            self.add_alias(match.group(k.call), match.group(k.response), slack_client, user_id, args)
            return True
        return

    def alias_remove_response(self, slack_client, user_id, msg_text):
        match = regular_expressions.alias_remove_response.match(msg_text)
        if match:
            self.remove_alias(match.group(k.call), slack_client, user_id)
            return True
        return False

    def process_message(self, slack_client, msg_text, user_id, channel, timestamp, args):
        if self.should_parse_message(slack_client, msg_text, user_id, channel):
            msg_text = msg_text.strip()

            if self.word_remove_response(slack_client, user_id, msg_text):
                return
            elif self.word_call_response(slack_client, user_id, msg_text):
                return
            elif self.alias_call_response(slack_client, user_id, msg_text, args):
                return
            elif self.alias_remove_response(slack_client, user_id, msg_text):
                return
            elif self.call_response(slack_client, user_id, msg_text):
                return
            elif self.remove_response(slack_client, user_id, msg_text):
                return


            response = self.get_response(slack_client, msg_text, user_id, channel, timestamp, args)
            if response:
                send_message(slack_client, response, channel)
