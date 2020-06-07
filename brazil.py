from urllib import request
from os import getcwd, path
import gzip
import datetime
import requests

from helpers import ensure_dirs


BRAZIL_DATA = 'https://data.brasil.io/dataset/covid19/caso.csv.gz'


def scrape_brazil():
    cwd = getcwd()
    brazil_dir = path.join(cwd, 'data', 'brazil')
    tmp_dir = path.join(cwd, 'tmp')

    ensure_dirs(brazil_dir, tmp_dir)

    gz_filename = path.join(tmp_dir, 'brazil.csv.gz')

    with open(gz_filename, 'wb') as gz_file:
        r = requests.get(BRAZIL_DATA, allow_redirects=True)
        gz_file.write(r.content)

    states = {}
    prev_state = ''
    header = ''
    curr_lines = []

    def write_file():
        with open(path.join(brazil_dir, f'{prev_state}.csv'), 'w') as state_file:
            state_file.writelines([header] + curr_lines)

    with gzip.open(gz_filename, 'rt') as f:
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
            states[state] = True

    write_file()

    with open(path.join(brazil_dir, 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents())


def get_readme_contents():
    return f"""## Brazil

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| State               | Dataset            |
| ------------------- | ------------------ |
| Acre                | [`ac.csv`](ac.csv) |
| Alagoas             | [`al.csv`](al.csv) |
| Amapá               | [`ap.csv`](ap.csv) |
| Amazonas            | [`am.csv`](am.csv) |
| Bahia               | [`ba.csv`](ba.csv) |
| Ceará               | [`ce.csv`](ce.csv) |
| Distrito Federal    | [`df.csv`](df.csv) |
| Espírito Santo      | [`es.csv`](es.csv) |
| Goiás               | [`go.csv`](go.csv) |
| Maranhão            | [`ma.csv`](ma.csv) |
| Mato Grosso         | [`mt.csv`](mt.csv) |
| Mato Grosso do Sul  | [`ms.csv`](ms.csv) |
| Minas Gerais        | [`mg.csv`](mg.csv) |
| Pará                | [`pa.csv`](pa.csv) |
| Paraíba             | [`pb.csv`](pb.csv) |
| Paraná              | [`pr.csv`](pr.csv) |
| Pernambuco          | [`pe.csv`](pe.csv) |
| Piauí               | [`pi.csv`](pi.csv) |
| Rio de Janeiro      | [`rj.csv`](rj.csv) |
| Rio Grande do Norte | [`rn.csv`](rn.csv) |
| Rio Grande do Sul   | [`rs.csv`](rs.csv) |
| Rondônia            | [`ro.csv`](ro.csv) |
| Roraima             | [`rr.csv`](rr.csv) |
| Santa Catarina      | [`sc.csv`](sc.csv) |
| São Paulo           | [`sp.csv`](sp.csv) |
| Sergipe             | [`se.csv`](se.csv) |
| Tocantins           | [`to.csv`](to.csv) |
"""
