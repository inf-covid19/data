import requests
from bs4 import BeautifulSoup
from os import getcwd, path, rename

import datetime
from helpers import ensure_dirs, ensure_consistency

URL = 'https://boliviasegura.gob.bo/wp-content/json/api.php'


def scrape_bolivia():
    cwd = getcwd()
    bolivia_dir = path.join(cwd, 'data', 'bolivia')
    tmp_dir = path.join(cwd, 'tmp')
    ensure_dirs(bolivia_dir, tmp_dir)

    page = requests.get(URL).json()
    
    today = str(datetime.date.today())
    day = str(datetime.datetime.strptime(page['fecha'], '%d/%m/%y %H:%M'))[:10]
    updated_files = []
    header = 'date,region_iso,province,city,place_type,cases,deaths,recovered\n'
    for dep in page['departamento'].keys():
        region = ISO_REGION[dep]
        iso = dep

        line = ','.join([
            day,
            iso,
            region,
            '',
            'departamento',
            str(page['departamento'][dep]['contador']['confirmados']),
            str(page['departamento'][dep]['contador']['decesos']),
            str(page['departamento'][dep]['contador']['recuperados'])
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
    toc = [f'| {name} | [`{iso.lower()}.csv`]({iso.lower()}.csv) |' for name, iso in REGION_ISO.items()]
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
