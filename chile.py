import requests
from bs4 import BeautifulSoup
import re
from os import getcwd, path, rename

import datetime
from helpers import ensure_dirs, ensure_consistency

URL = 'https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Chile'


def scrape_chile():
    cwd = getcwd()
    chile_dir = path.join(cwd, 'data', 'chile')
    tmp_dir = path.join(cwd, 'tmp')
    ensure_dirs(chile_dir, tmp_dir)

    today = str(datetime.date.today())
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    not_number_regexp = re.compile(r'\D')

    per_region_table = None
    tables = soup.find_all('table')

    for table in tables:
        headers = table.find_all('th')
        if len(headers) > 0 and 'Regiones' in headers[0].get_text():
            per_region_table = table
            break

    updated_files = []
    header = 'date,region,region_iso,province,city,place_type,cases,deaths\n'
    for tr in per_region_table.find_all('tr')[2:-1]:
        cols = [td.get_text() for td in tr.find_all('td')]
        if len(cols) != 13:
            continue

        iso = cols[1].strip()
        region = ISO_REGION[iso]

        line = ','.join([
            today,
            region,
            iso,
            '',
            '',
            'region',
            not_number_regexp.sub('', cols[6]),
            not_number_regexp.sub('', cols[11]),
        ])

        region_file = path.join(chile_dir, f'{iso.lower()}.csv')
        is_empty = not path.exists(region_file)

        with open(region_file, 'a+') as f:
            if is_empty:
                f.write(header)
            f.write(f'{line}\n')

        if not is_empty:
            updated_files.append(region_file)

    ensure_consistency(updated_files, lambda row: row[:5])

    with open(path.join(getcwd(), 'data', 'chile', 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents())


def get_readme_contents():
    toc = [f'| {name} | [`{iso.lower()}.csv`]({iso.lower()}.csv) |' for name,
           iso in REGION_ISO.items()]
    toc_contents = '\n'.join(toc)

    return f"""## Chile

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Region | Dataset |
| ------ | ------- |
{toc_contents}

"""


REGION_ISO = {
    "Tarapacá": "CL-TA",
    "Antofagasta": "CL-AN",
    "Atacama": "CL-AT",
    "Coquimbo": "CL-CO",
    "Araucanía": "CL-AR",
    "Valparaíso": "CL-VS",
    "O'Higgins": "CL-LI",
    "Maule": "CL-ML",
    "Biobío": "CL-BI",
    "Los Lagos": "CL-LL",
    "Aysén": "CL-AI",
    "Magallanes": "CL-MA",
    "Metropolitana": "CL-RM",
    "Los Ríos": "CL-LR",
    "Arica y Parinacota": "CL-AP",
    "Ñuble": "CL-NB",
}

ISO_REGION = {v: k for k, v in REGION_ISO.items()}
