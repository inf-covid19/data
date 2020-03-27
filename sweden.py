import requests
from bs4 import BeautifulSoup
from os import getcwd, path, rename

import datetime
from helpers import ensure_dirs


URL = 'https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/'


def scrape_sweden():
    cwd = getcwd()
    sweden_dir = path.join(cwd, 'data', 'sweden')
    tmp_dir = path.join(cwd, 'tmp')
    ensure_dirs(sweden_dir, tmp_dir)

    today = str(datetime.date.today())
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    header = 'date,county,county_iso,city,place_type,confirmed,deaths,estimated_population_2019,area_km2,confirmed_per_100k_inhabitants\n'

    updated_county_files = []

    for tr in soup.table.tbody.find_all('tr')[:-1]:
        cols = [td.get_text() for td in tr.find_all('td')]

        county = cols[0]
        iso = COUNTY_ISO_MAPPED[county].lower()
        values = [''.join(x.split(' ')) for x in cols[1:]]

        line = ','.join([
            today,
            county,
            iso.upper(),
            '',
            'county',
            values[0],
            values[3],
            str(COUNTY_POPULATION_MAPPED[county]),
            str(COUNTY_AREA_MAPPED[county]),
            values[1]
        ])

        county_file = path.join(sweden_dir, f'{iso}.csv')
        is_empty = not path.exists(county_file)

        with open(county_file, 'a+') as f:
            if is_empty:
                f.write(header)
            f.write(f'{line}\n')

        if not is_empty:
            updated_county_files.append(county_file)

    for county_file in updated_county_files:
        tmp_file = path.join(tmp_dir, 'tmp-county-sweden.csv')
        rename(county_file, tmp_file)

        with open(tmp_file, 'r') as tmp_f:
            with open(county_file, 'a+') as county_f:
                header = ''
                prev_data = None
                curr_line = ''
                for line in tmp_f:
                    if header == '':
                        header = line
                        county_f.write(header)
                        continue
                    data = line.split(',')[:5]
                    if prev_data is not None and prev_data != data:
                        county_f.write(curr_line)
                    curr_line = line
                    prev_data = data
                county_f.write(curr_line)



COUNTY_ISO_MAPPED = {
    'Stockholm': 'SE-AB',
    'Västerbotten': 'SE-AC',
    'Norrbotten': 'SE-BD',
    'Uppsala': 'SE-C',
    'Södermanland': 'SE-D',
    'Östergötland': 'SE-E',
    'Jönköping': 'SE-F',
    'Kronoberg': 'SE-G',
    'Kalmar': 'SE-H',
    'Gotland': 'SE-I',
    'Blekinge': 'SE-K',
    'Skåne': 'SE-M',
    'Halland': 'SE-N',
    'Västra Götaland': 'SE-O',
    'Värmland': 'SE-S',
    'Örebro': 'SE-T',
    'Västmanland': 'SE-U',
    'Dalarna': 'SE-W',
    'Gävleborg': 'SE-X',
    'Västernorrland': 'SE-Y',
    'Jämtland': 'SE-Z',
}

COUNTY_AREA_MAPPED = {
    'Stockholm': 6519.3,
    'Västerbotten': 55186.2,
    'Norrbotten': 98244.8,
    'Uppsala': 8207.2,
    'Södermanland': 6102.3,
    'Östergötland': 10602.0,
    'Jönköping': 10495.1,
    'Kronoberg': 8466.0,
    'Kalmar': 11217.8,
    'Gotland': 3151.4,
    'Blekinge': 2946.4,
    'Skåne': 11034.5,
    'Halland': 5460.7,
    'Västra Götaland': 23948.8,
    'Värmland': 17591.0,
    'Örebro': 8545.6,
    'Västmanland': 5145.8,
    'Dalarna': 28188.8,
    'Gävleborg': 18198.9,
    'Västernorrland': 21683.8,
    'Jämtland': 49341.2
}

# http://citypopulation.de/en/sweden/cities/mun/
COUNTY_POPULATION_MAPPED = {
    'Stockholm': 2344124,
    'Västerbotten': 270154,
    'Norrbotten': 250497,
    'Uppsala': 376354,
    'Södermanland': 294695,
    'Östergötland': 461583,
    'Jönköping': 360825,
    'Kronoberg': 199886,
    'Kalmar': 244670,
    'Gotland': 59249,
    'Blekinge': 159684,
    'Skåne': 1362164,
    'Halland': 329354,
    'Västra Götaland': 1709814,
    'Värmland': 281482,
    'Örebro': 302252,
    'Västmanland': 273929,
    'Dalarna': 287191,
    'Gävleborg': 286547,
    'Västernorrland': 245453,
    'Jämtland': 130280,
}
