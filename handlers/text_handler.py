from handlers.handler import Handler
from managers.config_manager import get_bot_name
from managers.user_manager import get_user_contact, register_user, unregister_user, get_user_by_id, get_registered_users
from handlers.handler_util.text_sender import send_text
from managers.message_manager import send_message_as_self
from util.regular_expressions import user_mention
import re
import util.constants as k

class Text(Handler):
    default_enabled = True
    name = 'text'

    def __init__(self):
        Handler.__init__(self)

    def get_help_msg(self):
        return 'This sends a text to the user mentioned in a text, if registered.\n' + \
               'usage is <' + get_bot_name() + ' ' + self.name + '>'

    def process_message(self, slack_client, msg_text, user_id, channel, timestamp, args):
        if 'unregister' in msg_text:
            unregister_user(user_id)
        elif 'register' in msg_text:
            try:
                to_num, from_num, acc, auth = msg_text.split('register')[1].strip(' ').split(' ')
            except KeyError:
                send_message_as_self(slack_client,
                                     "-sigh- At least try to get the formatting right, Zapp...",
                                     channel)
                send_message_as_self(slack_client,
                                     "@kif register <to_num> <from_num> <Twilio AccountSID> <Account Auth>",
                                     channel)
                return
            else:
                register_user(user_id, to_num, from_num, acc, auth)
        else:
            if '<!here>' in msg_text:
                msg_text = msg_text.replace('<!here>', '@here')
                users = get_registered_users()
                for user, info in users.items():
                    try:
                        user_info = get_user_contact(user)
                    except KeyError:
                        #not registered, move on
                        continue
                    else:
                        send_text(user_info, body=msg_text)

            mentioned = [m.strip('<@').strip('>') for m in re.findall(user_mention.pattern, msg_text)]
            for mention in mentioned:
                msg_text = msg_text.replace('<@{mention}>', mention)
            users = {mention: get_user_by_id(mention) for mention in mentioned}
            for mention, name in users.items():
                msg_text = msg_text.replace(mention, '@{name}')
            for user in mentioned:
                try:
                    user_info = get_user_contact(user)
                except KeyError:
                    #not registered, move on
                    continue
                else:
                    send_text(user_info, body=msg_text)