from util.file_IO import read_file, write_to_file
import user_manager
import message_manager
import util.constants as k
from util import regular_expressions
from config_manager import get_name
import channel_manager
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
    if user_manager.is_user_id(killers_id):
        message_manager.pm_user(slack_client, revive_msg, killers_id)
    else:
        message_manager.send_message(slack_client, revive_msg, channel_manager.get_default_channel())

def restart():
    if os.name == k.windows:
        subprocess.call('util/restart_scripts/restart.bat')
    elif os.name == 'posix':
        subprocess.call('./util/restart_scripts/restart.sh')

def process_message(slack_client, message):
    if k.text in message:
        regex_match = regular_expressions.two_words.match(message[k.text])
        if regex_match and regex_match.group(k.name) == get_name():
            if regex_match.group(k.command) == 'restart':
                message_text = 'restarting'

                channel_manager.update_channels(slack_client)
                message_manager.send_message_as_self(slack_client, message_text, message[k.channel])

                write_killer(message['user'])

                restart()
                return False
            elif regex_match.group(k.command) == 'die':
                message_text = 'dieing'

                channel_manager.update_channels(slack_client)
                message_manager.send_message_as_self(slack_client, message_text, message[k.channel])

                write_killer(message['user'])

                return False
    return True
