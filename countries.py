from urllib import request
from os import getcwd, path

COUNTRIES_DATA = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'


def scrape_countries():
    cwd = getcwd()
    prev_country = ''
    header = ''
    curr_lines = []

    for line_bin in request.urlopen(COUNTRIES_DATA):
        line = line_bin.decode('iso-8859-1')
        if header == '':
            header = line
            continue
        country = line.split(',')[6].lower()
        if len(prev_country) > 0 and country != prev_country:
            with open(path.join(cwd, 'data', 'countries', f'{prev_country}.csv'), 'w') as country_file:
                country_file.writelines([header] + curr_lines)
            curr_lines = []
        curr_lines.append(line)
        prev_country = country