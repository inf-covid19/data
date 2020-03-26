from os import getcwd, makedirs, path


def ensure_dirs(*dirs):
    for d in dirs:
        try:
            makedirs(d)
        except:
            pass
