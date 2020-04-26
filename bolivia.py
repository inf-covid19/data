import requests
from bs4 import BeautifulSoup
from os import getcwd, path, rename

import datetime
from helpers import ensure_dirs, ensure_consistency

URL = 'https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Bolivia'


def scrape_bolivia():
    cwd = getcwd()
    bolivia_dir = path.join(cwd, 'data', 'bolivia')
    tmp_dir = path.join(cwd, 'tmp')
    ensure_dirs(bolivia_dir, tmp_dir)

    today = str(datetime.date.today())
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    tables = soup.find_all('table')

    per_dep_table = None
    per_city_table = None

    for table in tables:
        if table.caption and 'Epidemiología' in table.caption.get_text():
            per_dep_table = table
            continue

        headers = table.find_all('th')
        if len(headers) > 0 and 'Municipios Bolivianos' in headers[0].get_text():
            per_city_table = table

    updated_files = []
    header = 'date,region_iso,region,province,city,place_type,cases,deaths,recovered\n'

    for tr in per_dep_table.tbody.find_all('tr')[1:-1]:
        cols = [td.get_text().strip() for td in tr.find_all('td')]

        region = cols[0]
        iso = REGION_ISO[region]

        line = ','.join([
            today,
            iso,
            region,
            '',
            '',
            'departamento',
            cols[1],
            cols[2],
            cols[3]
        ])

        region_file = path.join(bolivia_dir, f'{iso.lower()}.csv')
        is_empty = not path.exists(region_file)

        with open(region_file, 'a+') as f:
            if is_empty:
                f.write(header)
            f.write(f'{line}\n')

        if not is_empty: 
            updated_files.append(region_file)

    ensure_consistency(updated_files, lambda row: row[:5])

    with open(path.join(getcwd(), 'data', 'bolivia', 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents())


def get_readme_contents():
    toc = [f'| {name} | [`{iso.lower()}.csv`]({iso.lower()}.csv) |' for name,
           iso in REGION_ISO.items()]
    toc_contents = '\n'.join(toc)

    return f"""## Bolivia

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Region | Dataset |
| ------ | ------- |
{toc_contents}

"""


REGION_ISO = {
    "La Paz": "lp",
    "Cochabamba": "cb",
    "Santa Cruz": "sc",
    "Oruro": "or",
    "Potosí": "pt",
    "Tarija": "tj",
    "Chuquisaca": "ch",
    "Beni": "bn",
    "Pando": "pn"
}

ISO_REGION = {
    "lp": "La Paz",
    "cb": "Cochabamba",
    "sc": "Santa Cruz",
    "or": "Oruro",
    "pt": "Potosí",
    "tj": "Tarija",
    "ch": "Chuquisaca",
    "bn": "Beni",
    "pn": "Pando"
}
