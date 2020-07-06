import requests
import re
from bs4 import BeautifulSoup
from os import getcwd, path, rename

import datetime
from helpers import ensure_dirs, ensure_consistency

URL = 'https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Per%C3%BA'


def scrape_peru():
    cwd = getcwd()
    peru_dir = path.join(cwd, 'data', 'peru')
    tmp_dir = path.join(cwd, 'tmp')
    ensure_dirs(peru_dir, tmp_dir)

    not_number_regexp = re.compile(r'\D')

    today = str(datetime.date.today())
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    tables = soup.find_all('table', {'class': 'sortable'})
    per_departament_table = None

    for table in tables:
        headers = [th.get_text().strip() for th in table.find_all('th')]
        if len(headers) > 0 and 'Departamentos' == headers[0]:
            per_departament_table = table

    updated_files = []
    header = 'date,iso,region,city,place_type,cases,deaths\n'

    mapped = {}

    for tr in per_departament_table.tbody.find_all('tr'):
        cols = [td.get_text().strip() for td in tr.find_all('td')]
        if len(cols) != 9:
            continue

        departament = cols[0]

        cases = int(not_number_regexp.sub('', cols[2]))
        deaths = int(not_number_regexp.sub('', cols[4]))

        if 'Lima' in departament:
            departament = 'Lima'
            if 'Lima' in mapped:
                _cases, _deaths = mapped['Lima']
                cases += _cases
                deaths += _deaths
            else:
                mapped['Lima'] = (cases, deaths)
                continue

        iso = DEPARTAMENT_ISO[departament]

        line = ','.join([
            today,
            iso,
            departament,
            '',
            'departamento',
            str(cases),
            str(deaths),
        ])

        departament_file = path.join(peru_dir, f'{iso.lower()}.csv')
        is_empty = not path.exists(departament_file)

        with open(departament_file, 'a+') as f:
            if is_empty:
                f.write(header)
            f.write(f'{line}\n')

        if not is_empty:
            updated_files.append(departament_file)

    ensure_consistency(updated_files, lambda row: row[:4])

    with open(path.join(getcwd(), 'data', 'peru', 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents())


def get_readme_contents():
    toc = [f'| {name} | [`{iso.lower()}.csv`]({iso.lower()}.csv) |' for name,
           iso in DEPARTAMENT_ISO.items()]
    toc_contents = '\n'.join(toc)

    return f"""## Peru

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Departament | Dataset |
| ----------- | ------- |
{toc_contents}

"""


DEPARTAMENT_ISO = {
    'Amazonas': 'PE-AMA',
    'Áncash': 'PE-ANC',
    'Apurímac': 'PE-APU',
    'Arequipa': 'PE-ARE',
    'Ayacucho': 'PE-AYA',
    'Cajamarca': 'PE-CAJ',
    'Callao': 'PE-CAL',
    'Cusco': 'PE-CUS',
    'Huancavelica': 'PE-HUV',
    'Huánuco': 'PE-HUC',
    'Ica': 'PE-ICA',
    'Junín': 'PE-JUN',
    'La Libertad': 'PE-LAL',
    'Lambayeque': 'PE-LAM',
    'Lima': 'PE-LIM',
    'Loreto': 'PE-LOR',
    'Madre de Dios': 'PE-MDD',
    'Moquegua': 'PE-MOQ',
    'Pasco': 'PE-PAS',
    'Piura': 'PE-PIU',
    'Puno': 'PE-PUN',
    'San Martín': 'PE-SAM',
    'Tacna': 'PE-TAC',
    'Tumbes': 'PE-TUM',
    'Ucayali': 'PE-UCA',
}
