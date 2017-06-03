import os.path
import json

def _write_if_nothing(file_path):
    if not os.path.isfile(file_path):
        write_to_file(file_path, '')

def write_to_file(file_path, contents):
    with open(file_path, 'w') as f:
        f.write(contents)

def append_to_file(file_path, addition):
    with open(file_path, 'a') as f:
        f.write(addition)

def read_file(file_path):
    _write_if_nothing(file_path)

    with open(file_path, 'r') as f:
        return f.read()

def write_to_json(file_path, contents):
    with open(file_path, 'w') as f:
        json.dump(contents, f)

def read_from_json(file_path):
    _write_if_nothing(file_path)

    with open(file_path) as f:
        return json.load(f)
