import requests
from bs4 import BeautifulSoup
from os import getcwd, path, rename

import datetime
from helpers import ensure_dirs, ensure_consistency

URL = 'https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/'


def scrape_chile():
    cwd = getcwd()
    chile_dir = path.join(cwd, 'data', 'chile')
    tmp_dir = path.join(cwd, 'tmp')
    ensure_dirs(chile_dir, tmp_dir)

    today = str(datetime.date.today())
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    updated_files = []
    header = 'date,region,region_iso,province,city,place_type,cases,deaths\n'
    for tr in soup.table.tbody.find_all('tr')[3:-1]:
        cols = [td.get_text() for td in tr.find_all('td')]
        
        region = cols[0]
        iso = REGION_ISO[region]

        line = ','.join([
            today,
            region,
            iso,
            '',
            '',
            'region',
            cols[1],
            cols[4]
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
    toc = [f'| {name} | [`{iso.lower()}.csv`]({iso.lower()}.csv) |' for name, iso in REGION_ISO.items()]
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
    "O’Higgins": "CL-LI",
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
