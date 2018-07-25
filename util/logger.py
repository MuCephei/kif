from datetime import datetime
from util.file_IO import write_to_file, read_file
import util.constants as k
import os
import traceback

def _get_path(file):
    return k.log + '/' + file

def write_to_log(exc_info):
    type_, value_, traceback_ = exc_info
    trace = traceback.format_tb(traceback_)
    message = str(type_) + '\n' + str(value_) + '\n' + ''.join(trace)
    time = str(datetime.now()).replace(' ', '_').replace('.', '_').replace(':', '_').replace('-', '_')
    write_to_file(_get_path(time), message)

def get_log_list(n=0):
    logs = os.listdir(k.log)
    if not logs:
        return []
    if n:
        return sorted(logs, reverse=True)[:n]
    else:
        return sorted(logs, reverse=True)

def delete_logs():
    logs = get_log_list()
    if logs:
        for log in logs:
            os.remove(log)
        return len(logs)

def get_log(n):
    logs = get_log_list(n + 1)
    if logs:
        return read_file(_get_path(logs[-1]))
    else:
        return 'No logs found'

def get_most_recent_log():
    return get_log(1)
