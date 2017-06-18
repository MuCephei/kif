from handlers import call_response_handler, config_handler, id_handler, sigh_handler, crash_handler
from config_manager import update_conf
from user_manager import get_user_by_id
from config_manager import get_name
import util.constants as k

class HandlerManager:

    def _get_handler_conf(self, name):
        if name in self.handlers_by_name:
            return self.handlers_by_name[name].conf
        return False

    def _update_handler_conf(self, name, new_conf):
        update_conf(name, new_conf)
        if name in self.handlers_by_name:
            self.handlers_by_name[name].reload()
            return True
        return False

    def _reset_handler_conf(self, name):
        if name in self.handlers_by_name:
            conf = self.handlers_by_name[name].make_config()
            return self._update_handler_conf(name, conf)
        return False

    def _is_name_of_handler(self, name):
        return name in self.handlers_by_name

    def __init__(self):
        enabled = config_handler.Config(self._get_handler_conf,
                                        self._update_handler_conf,
                                        self._is_name_of_handler,
                                        self._reset_handler_conf)
        self.handlers = [sigh_handler.Sigh(),
                         id_handler.Id(),
                         enabled,
                         call_response_handler.CallResponse(),
                         crash_handler.Crash()]
        self.handlers_by_name = {value.name: value for value in self.handlers}

    def process_message(self, slack_client, message):
        if k.user in message and get_user_by_id(message[k.user], slack_client) != get_name():
            for h in self.handlers:
                h.process_message(slack_client, message)
