from os import getcwd, makedirs, path, rename


def backup_file(filename):
    cwd = getcwd()
    _file = filename.replace(cwd+'/', '').replace('/', '--')
    tmp_file = path.join(
        cwd,
        'tmp',
        f'{_file}.bak'
    )
    rename(filename, tmp_file)
    return tmp_file


def ensure_dirs(*dirs):
    for d in dirs:
        try:
            makedirs(d)
        except:
            pass


def ensure_consistency(updated_files, identifier):
    for update_file in updated_files:
        tmp_file = backup_file(update_file)

        with open(tmp_file, 'r') as tmp_f:
            with open(update_file, 'a+') as update_f:
                header = ''
                prev_id = None
                latest_line = ''
                for line in tmp_f:
                    if header == '':
                        header = line
                        update_f.write(header)
                        continue
                    _id = identifier(line.split(','))
                    if prev_id is not None and prev_id != _id:
                        update_f.write(latest_line)
                    latest_line = line
                    prev_id = _id
                update_f.write(latest_line)
