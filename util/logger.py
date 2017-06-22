from datetime import datetime
from file_IO import write_to_file, read_file
import constants as k
import os
import traceback

def _get_path(file):
    return k.log + '/' + file

def write_to_log(exc_info):
    type_, value_, traceback_ = exc_info
    trace = traceback.format_tb(traceback_)
    message = str(type_) + '\n' + str(value_) + '\n' + ''.join(trace)
    time = str(datetime.now()).replace(' ', '_').replace('.', '_').replace(':', '_')
    write_to_file(_get_path(time), message)

def get_log_list(n=0):
    logs = os.listdir(k.log)
    if n:
        return sorted(logs)[:n]
    else:
        return sorted(logs)

def get_most_recent_log():
    return read_file(_get_path(get_log_list(1)))

def get_specific_log(name):
    logs = os.listdir(k.log)
    if name in logs:
        return read_file(_get_path(name))
    return 'No such log found'
