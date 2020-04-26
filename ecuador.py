import requests
import re
from bs4 import BeautifulSoup
from os import getcwd, path, rename

import datetime
from helpers import ensure_dirs, ensure_consistency

URL = 'https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Ecuador'


def scrape_ecuador():
    cwd = getcwd()
    ecuador_dir = path.join(cwd, 'data', 'ecuador')
    tmp_dir = path.join(cwd, 'tmp')
    ensure_dirs(ecuador_dir, tmp_dir)
    
    not_number_regexp = re.compile(r'\D')

    today = str(datetime.date.today())
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    tables = soup.find_all('table', {'class': 'sortable'})
    per_province_table = None

    for table in tables:
        headers = [th.get_text().strip() for th in table.find_all('th')]
        if len(headers) > 0 and 'Provincias' == headers[0]:
            per_province_table = table

    updated_files = []
    header = 'date,iso,province,city,place_type,cases,deaths\n'

    for tr in per_province_table.tbody.find_all('tr'):
        cols = [td.get_text().strip() for td in tr.find_all('td')]
        if len(cols) != 3:
            continue

        province = cols[0]
        iso = PROVINCE_ISO[province]

        line = ','.join([
            today,
            iso,
            province,
            '',
            'province',
           not_number_regexp.sub('', cols[1]),
           not_number_regexp.sub('', cols[2]),
        ])

        province_file = path.join(ecuador_dir, f'{iso.lower()}.csv')
        is_empty = not path.exists(province_file)

        with open(province_file, 'a+') as f:
            if is_empty:
                f.write(header)
            f.write(f'{line}\n')

        if not is_empty:
            updated_files.append(province_file)

    ensure_consistency(updated_files, lambda row: row[:4])

    with open(path.join(getcwd(), 'data', 'ecuador', 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents())


def get_readme_contents():
    toc = [f'| {name} | [`{iso.lower()}.csv`]({iso.lower()}.csv) |' for name,
           iso in PROVINCE_ISO.items()]
    toc_contents = '\n'.join(toc)

    return f"""## Ecuador

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Province | Dataset |
| -------- | ------- |
{toc_contents}

"""


PROVINCE_ISO = {
    'Azuay': 'EC-A',
    'Bolívar': 'EC-B',
    'Cañar': 'EC-F',
    'Carchi': 'EC-C',
    'Chimborazo': 'EC-H',
    'Cotopaxi': 'EC-X',
    'El Oro': 'EC-O',
    'Esmeraldas': 'EC-E',
    'Galápagos': 'EC-W',
    'Guayas': 'EC-G',
    'Imbabura': 'EC-I',
    'Loja': 'EC-L',
    'Los Ríos': 'EC-R',
    'Manabí': 'EC-M',
    'Morona Santiago': 'EC-S',
    'Napo': 'EC-N',
    'Orellana': 'EC-D',
    'Pastaza': 'EC-Y',
    'Pichincha': 'EC-P',
    'Santa Elena': 'EC-SE',
    'Santo Domingo de los Tsáchilas': 'EC-SD',
    'Sucumbíos': 'EC-U',
    'Tungurahua': 'EC-T',
    'Zamora Chinchipe': 'EC-Z',
}
