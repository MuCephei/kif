from util.file_IO import read_file, write_to_file
import managers.user_manager
import managers.message_manager
import util.constants as k
from util import regular_expressions
from managers.config_manager import get_bot_name
import managers.channel_manager
import subprocess
import os

killer_id_file = 'killer_id'
revive_msg = "I'm alive"

def write_killer(killer_id):
    write_to_file(killer_id_file, killer_id)

def get_killer_id():
    return read_file(killer_id_file).strip()

def revive(slack_client):
    killers_id = get_killer_id()
    if killers_id and managers.user_manager.is_user_id(killers_id):
        managers.message_manager.pm_user(slack_client, revive_msg, killers_id)
    else:
        managers.message_manager.send_message(slack_client, revive_msg, managers.channel_manager.get_default_channel())

def restart():
    if os.name == k.windows:
        subprocess.call('.\\util\\restart_scripts\\restart.bat')
    elif os.name == 'posix':
        subprocess.call('./util/restart_scripts/restart.sh')

def process_message(slack_client, msg_text, user_id, channel, timestamp, args):
    if msg_text:
        regex_match = regular_expressions.words[2].match(msg_text)
        if regex_match and regex_match.group(k.first) == get_bot_name():
            if regex_match.group(k.second) == 'restart':
                message_text = 'restarting'

                managers.channel_manager.update_channels(slack_client)
                managers.message_manager.send_message_as_self(slack_client, message_text, channel)

                write_killer(user_id)

                restart()
                return False
            elif regex_match.group(k.second) == 'die':
                message_text = 'dieing'

                managers.channel_manager.update_channels(slack_client)
                managers.message_manager.send_message_as_self(slack_client, message_text, channel)

                write_killer(user_id)

                return False
    return True
