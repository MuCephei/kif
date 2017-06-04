enabled = 'enabled'

def make_config(_enabled, args=None):
    conf = {enabled: _enabled}
    for a in args:
        conf[a[0]] = a[1]
    return conf
