import util.file_IO as io
from util.api_calls import get_channels, get_groups, get_ims
import user_manager

_channel_manager_folder = 'channel_manager'
_channel_names = _channel_manager_folder + '/ChannelNames.json'
_channel_ids = _channel_manager_folder + '/ChannelIds.json'
_default = _channel_manager_folder + '/default'

def update_channels(slack_client):
    channels = get_channels(slack_client)
    groups = get_groups(slack_client)
    ims = get_ims(slack_client)
    channel_names = {}
    channel_ids = {}

    if channels['ok']:
        for channel in channels['channels']:
            channel_names[channel['id']] = channel['name']
            channel_ids[channel['name']] = channel['id']

    if groups['ok']:
        for group in groups['groups']:
            channel_names[group['id']] = group['name']
            channel_ids[group['name']] = group['id']

    if ims['ok']:
        for im in ims['ims']:
            channel_names[im['id']] = im['user']
            channel_ids[im['user']] = im['id']

    io.write_to_json(_channel_names, channel_names)
    io.write_to_json(_channel_ids, channel_ids)

def get_channel_by_id(channel_id, slack_client=None):
    channel_names = io.read_from_json(_channel_names)

    if channel_id in channel_names:
        return str(channel_names[channel_id])
    elif slack_client:
        update_channels(slack_client)
        if channel_id in channel_names:
            return str(channel_names[channel_id])
    return io.read_file(_default)

def get_channel_by_name(channel_name, slack_client=None):
    channel_ids = io.read_from_json(_channel_ids)

    if channel_name in channel_ids:
        return str(channel_ids[channel_name])
    elif slack_client:
        update_channels(slack_client)
        if channel_name in channel_ids:
            return str(channel_ids[channel_name])
    return io.read_file(_default)

def get_channel_by_user(user, slack_client=None):
    user_id = user_manager.get_user_by_name(user, slack_client)
    if not user_id:
        user_id = user
    return get_channel_by_name(user_id, slack_client)