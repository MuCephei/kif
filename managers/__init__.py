from util.directory import mkdir
from .channel_manager import _channel_manager_folder
from .user_manager import _user_manager_folder
from .config_manager import _conf_manager_folder

mkdir(_channel_manager_folder)
mkdir(_user_manager_folder)
mkdir(_conf_manager_folder)