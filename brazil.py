from urllib import request
from os import getcwd, path
import gzip

from helpers import ensure_dirs


BRAZIL_DATA = 'https://data.brasil.io/dataset/covid19/caso.csv.gz'


def scrape_brazil():
    cwd = getcwd()
    brazil_dir = path.join(cwd, 'data', 'brazil')
    tmp_dir = path.join(cwd, 'tmp')

    ensure_dirs(brazil_dir, tmp_dir)

    gz_file = path.join(tmp_dir, 'brazil.csv.gz')
    request.urlretrieve(BRAZIL_DATA, gz_file)

    prev_state = ''
    header = ''
    curr_lines = []

    def write_file():
        with open(path.join(brazil_dir, f'{prev_state}.csv'), 'w') as state_file:
            state_file.writelines([header] + curr_lines)

    with gzip.open(gz_file, 'rt') as f:
        for line in f:
            if header == '':
                header = line
                continue

            state = line.split(',')[1].lower()
            if len(prev_state) > 0 and state != prev_state:
                write_file()
                curr_lines = []

            curr_lines.append(line)
            prev_state = state

    write_file()
