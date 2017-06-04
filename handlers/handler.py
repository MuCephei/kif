from util.file_IO import write_json_if_nothing, read_from_json
from util.directory import mkdir
import config

class Handler:
    handler_folder = 'handler_conf'
    config_file = 'conf'
    name = 'handler'
    default_enabled = False

    def __init__(self):
        self.folder = self.get_path()
        self.conf = self.make_config()
        self.setup()

    def make_config(self):
        return config.make_config(self.default_enabled)

    def get_path(self):
        return self.handler_folder + '/' + self.name

    def get_config_path(self):
        return self.get_path() + '/' + self.config_file

    def setup(self):
        mkdir(self.folder)
        path = self.get_config_path()
        write_json_if_nothing(path, self.conf)
        self.conf = read_from_json(path)

    def should_trigger(self, msg):
        return self.conf[config.enabled]

    def trigger(self, slack_client, message):
        pass

