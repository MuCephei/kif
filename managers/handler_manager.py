from handlers import sigh_handler, id_handler, enabled_handler
from config_manager import update_conf

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

    def _is_name_of_handler(self, name):
        return name in self.handlers_by_name

    def __init__(self):
        enabled = enabled_handler.Enabled(self._get_handler_conf,
                                          self._update_handler_conf,
                                          self._is_name_of_handler)
        self.handlers = [sigh_handler.Sigh(), id_handler.Id(), enabled]
        self.handlers_by_name = {value.name: value for value in self.handlers}

    def process_message(self, slack_client, message):
        for h in self.handlers:
            if h.should_trigger(message):
                h.trigger(slack_client, message)