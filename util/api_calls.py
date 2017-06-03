_post_msg = 'chat.postMessage'
_channels = 'channels.list'
_groups = 'groups.list'
_ims = 'im.list'
_users = 'users.list'

def write_msg(slack_client, msg, channel):
    slack_client.api_call(
        _post_msg,
        channel = channel,
        text = msg,
        as_user = True)

def get_channels(slack_client):
    return slack_client.api_call(_channels)

def get_groups(slack_client):
    return slack_client.api_call(_groups)

def get_ims(slack_client):
    return slack_client.api_call(_ims)

def get_users(slack_client):
    return slack_client.api_call(_users)