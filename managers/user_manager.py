import util.file_IO as io
from util.api_calls import get_users
import util.constants as k

_user_manager_folder = 'user_manager'
_user_names = _user_manager_folder + '/Usernames.json'
_user_ids = _user_manager_folder + '/UserIds.json'
_my_id = _user_manager_folder + '/my_id'
_registered_users = _user_manager_folder + '/RegisteredUsers.json'


def update_names(slack_client):
    users = get_users(slack_client)
    user_names = {}
    user_ids = {}
    for user in users['members']:
        user_names[user[k.id]] = user[k.name]
        user_ids[user[k.name]] = user[k.id]

    my_id = slack_client.server.login_data[k.self][k.id]

    io.write_to_file(_my_id, my_id)
    io.write_to_json(_user_names, user_names)
    io.write_to_json(_user_ids, user_ids)


def is_user_id(user_id):
    user_names = io.read_from_json(_user_names)
    return user_id in user_names


def get_registered_users():
    return io.read_from_json(_registered_users)


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


def get_my_id(slack_client):
    my_id = io.read_file(_my_id)
    if not my_id:
        update_names(slack_client)
        my_id = io.read_file(_my_id)
    return my_id


def get_user_contact(user_id):
    user_dict = io.read_from_json(_registered_users)
    return user_dict[user_id]


def register_user(user_id, to_num, from_num, accountSID, auth):
    curr_users = io.read_from_json(_registered_users)
    # it does in place replacing, if you need to update your number(s)
    curr_users[user_id] = {'to_num': to_num,
                           'from_num': from_num,
                           'AccountSID': accountSID,
                           'Auth': auth
                           }
    io.write_to_json(_registered_users, curr_users)

def unregister_user(user_id):
    curr_users = io.read_from_json(_registered_users)
    try:
        curr_users.pop(user_id)
    except:
        pass
        # if they're not subscribed, whatever
    io.write_to_json(_registered_users, curr_users)