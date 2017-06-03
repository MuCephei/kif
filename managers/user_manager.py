import util.file_IO as io
from util.api_calls import get_users

_user_manager_folder = 'user_manager'
_user_names = _user_manager_folder + '/Usernames.json'
_user_ids = _user_manager_folder + '/UserIds.json'

def update_names(slack_client):
    users = get_users(slack_client)
    user_names = {}
    user_ids = {}
    for user in users['members']:
        user_names[user['id']] = user['name']
        user_ids[user['name']] = user['id']
    io.write_to_json(_user_names, user_names)
    io.write_to_json(_user_ids, user_ids)

def get_user_by_id(user_id, slack_client=None):
    user_names = io.read_from_json(_user_names)

    if user_id in user_names:
        return str(user_names[user_id])
    elif slack_client:
        update_names(slack_client)
        if user_id in user_names:
            return str(user_names[user_id])
    return None

def get_user_by_name(user_name, slack_client=None):
    user_ids = io.read_from_json(_user_ids)

    if user_name in user_ids:
        return str(user_ids[user_name])
    elif slack_client:
        update_names(slack_client)
        if user_name in user_ids:
            return str(user_ids[user_name])
    return None

def get_users_mentioned(message):
    user_ids = io.read_from_json(_user_ids)

    mentioned_users = set()
    for token in message.split():
        if token in user_ids:
            mentioned_users.add(token)
    return mentioned_users