import time
import traceback
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


def executor(fn, *args, **kwargs):
    trace_info = None

    print(f'[{fn.__name__}] Starting...')
    start_time = time.time()

    r = None
    try:
        r = fn(*args, **kwargs)
    except Exception:
        trace_info = traceback.format_exc().splitlines()
    elapsed_time = time.time() - start_time

    if trace_info is None:
        print(f'[{fn.__name__}] Done in {elapsed_time:.3f}s!')
    else:
        print(f'[{fn.__name__}] Failed in {elapsed_time:.3f}s!')
        print(f'[{fn.__name__}]  ' + f'\n[{fn.__name__}]  '.join(trace_info))
    print('')

    return r
