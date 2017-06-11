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
    help_msg = 'To add a call type a message with the following format (Caps are important)\n' \
               '"Call:<Your text here> Response:<Response Here>"\n' \
               'To remove a call, use the following format\n' \
               '"Remove:<Your text here> Response:<Response Here>"\n' \
               'To stop the bot from responding from the module\n' \
               '"stop ' + name + '"\n' \
               'To start the bot responding again\n' \
               '"start ' + name + '"\n' \
               'Note that the "" and <> symbols are not part of the required message'
    triggers = (Handler.trigger_tag, {'help': [help_msg]})
    opt_out = 'opt_out'

    def __init__(self):
        Handler.__init__(self)

    def make_config(self):
        args = [self.triggers] + [(self.opt_out, [])]
        return config.make_config(self.default_enabled, args)

    def get_response(self, msg_text):
        response = ''
        for key, values in self.conf[Handler.trigger_tag].iteritems():
            if key in msg_text:
                response = response + random.choice(values) + '\n'
        return response

    def add_call_response(self, call, response):
        if call in self.conf[Handler.trigger_tag]:
            if response not in self.conf[Handler.trigger_tag][call]:
                self.conf[Handler.trigger_tag][call].append(response)
        else:
            self.conf[Handler.trigger_tag][call] = [response]
        update_conf(self.name, self.conf)

    def remove_call_response(self, call, response):
        if call in self.conf[Handler.trigger_tag]:
            if response in self.conf[Handler.trigger_tag][call]:
                self.conf[Handler.trigger_tag][call].remove(response)
                if not len(self.conf[Handler.trigger_tag][call]):
                    self.conf[Handler.trigger_tag].pop(call)
        update_conf(self.name, self.conf)

    def user_opt_out(self, user_id):
        if user_id not in self.conf[self.opt_out]:
            self.conf[self.opt_out].append(user_id)
        update_conf(self.name, self.conf)

    def user_opt_in(self, user_id):
        if user_id in self.conf[self.opt_out]:
            self.conf[self.opt_out].remove(user_id)
        update_conf(self.name, self.conf)

    def process_message(self, slack_client, message):
        if not self.conf[config.enabled]:
            return
        if k.text not in message or k.user not in message or k.channel not in message:
            return
        user_id = message[k.user]
        msg_text = message[k.text]
        regex_match = regular_expressions.two_words.match(msg_text)
        if user_id in self.conf[self.opt_out]:
            #check for opt-in
            if regex_match:
                if regex_match.group(k.command) == k.start and regex_match.group(k.name) == self.name:
                    self.user_opt_in(user_id)
                    pm_user(slack_client, 'Opted in', user_id)

        else:
            #check for opt-out
            if regex_match:
                if regex_match.group(k.command) == k.stop and regex_match.group(k.name) == self.name:
                    self.user_opt_out(user_id)
                    pm_user(slack_client, 'Opted out', user_id)
                    return

            call_response_match = regular_expressions.call_response.match(msg_text)
            if call_response_match:
                self.add_call_response(call_response_match.group(k.call),
                                       call_response_match.group(k.response))
                return

            remove_response_match = regular_expressions.remove_response.match(msg_text)
            if remove_response_match:
                self.remove_call_response(remove_response_match.group(k.remove),
                                          remove_response_match.group(k.response))
                return

            response = self.get_response(msg_text)
            if response:
                send_message(slack_client, response, message[k.channel])
