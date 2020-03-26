from urllib import request
from os import getcwd, path

from helpers import ensure_dirs

COUNTRIES_DATA = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'


def scrape_countries():
    cwd = getcwd()
    countries_dir = path.join(cwd, 'data', 'countries')
    ensure_dirs(countries_dir)

    prev_country = ''
    header = ''
    curr_lines = []

    def write_file():
        with open(path.join(countries_dir, f'{prev_country}.csv'), 'w') as country_file:
            country_file.writelines([header] + curr_lines)

    for line_bin in request.urlopen(COUNTRIES_DATA):
        line = line_bin.decode('iso-8859-1')

        if header == '':
            header = line
            continue

        country = line.split(',')[6].lower()
        if len(prev_country) > 0 and country != prev_country:
            write_file()
            curr_lines = []

        curr_lines.append(line)
        prev_country = country

    write_file()
