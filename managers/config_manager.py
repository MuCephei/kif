from util.config import make_config
from util import file_IO

_conf_manager_folder = 'conf'
_main_conf_path = _conf_manager_folder + '/main'
name_tag = 'name'
default_name = 'kif'
edit_permissions = 'edit'
default_editors = []
icon_tag = 'icon'
default_icon = ':robot_face:'

def _make_default_conf():
    args = [(name_tag, default_name),
            (edit_permissions, default_editors),
            (icon_tag, default_icon)]
    return make_config(True, args = args)

def get_default_conf():
    file_IO.write_json_if_nothing(_main_conf_path, fct = _make_default_conf)
    return file_IO.read_from_json(_main_conf_path)

def get_name():
    conf = get_default_conf()
    if name_tag in conf:
        return conf[name_tag]
    return default_name

def get_icon():
    conf = get_default_conf()
    if icon_tag in conf:
        return conf[icon_tag]
    return default_icon

def can_user_edit(user_id):
    conf = get_default_conf()
    return edit_permissions in conf and user_id in conf[edit_permissions]

def _get_path(name):
    return _conf_manager_folder + '/' + name

def get_config(name, default_conf='{}', fct=None):
    path = _get_path(name)
    file_IO.write_json_if_nothing(path, msg = default_conf, fct = fct)
    return file_IO.read_from_json(path)

def update_conf(name, new_conf):
    path = _get_path(name)
    file_IO.write_to_json(path, new_conf)

