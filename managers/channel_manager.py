import util.file_IO as io
from util.api_calls import get_channels, get_groups, get_ims
import util.constants as k

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

    if channels[k.ok]:
        for channel in channels['channels']:
            channel_names[channel[k.id]] = channel[k.name]
            channel_ids[channel[k.name]] = channel[k.id]

    if groups[k.ok]:
        for group in groups['groups']:
            channel_names[group[k.id]] = group[k.name]
            channel_ids[group[k.name]] = group[k.id]

    if ims[k.ok]:
        for im in ims['ims']:
            channel_names[im[k.id]] = im[k.user]
            channel_ids[im[k.user]] = im[k.id]

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
    return get_default_channel()

def get_channel_by_name(channel_name, slack_client=None):
    channel_ids = io.read_from_json(_channel_ids)

    if channel_name in channel_ids:
        return str(channel_ids[channel_name])
    elif slack_client:
        update_channels(slack_client)
        if channel_name in channel_ids:
            return str(channel_ids[channel_name])
    return get_default_channel()

def get_channel_by_user_id(user_id, slack_client=None):
    return get_channel_by_name(user_id, slack_client)

def get_default_channel():
    return io.read_file(_default)
