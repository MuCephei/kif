from os import path, makedirs

def mkdir(folder):
    if not path.exists(folder):
        makedirs(folder)