from urllib import request
from os import getcwd, path
import datetime

from helpers import ensure_dirs

COUNTRIES_DATA = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'


def scrape_countries():
    cwd = getcwd()
    countries_dir = path.join(cwd, 'data', 'countries')
    ensure_dirs(countries_dir)

    countries = {}
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

        country_name = line.split(',')[6]
        country = country_name.lower()
        if len(prev_country) > 0 and country != prev_country:
            write_file()
            curr_lines = []

        curr_lines.append(line)
        prev_country = country
        countries[country_name] = True

    write_file()

    with open(path.join(countries_dir, 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents(countries))


def get_readme_contents(countries):
    countries_datasets = [(country.replace('_', ' '), country.lower()+'.csv') for country in countries]
    toc = [f'| {name} | [`{dataset}`]({dataset}) |' for name, dataset in countries_datasets]
    toc_contents = '\n'.join(toc)
    return f"""## Countries

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Country | Dataset |
| ------ | ------- |
{toc_contents}
"""