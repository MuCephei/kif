def make_config(args=list()):
    conf = dict()
    for a in args:
        conf[a[0]] = a[1]
    return conf
