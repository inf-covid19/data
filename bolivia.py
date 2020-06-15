import requests
from bs4 import BeautifulSoup
from os import getcwd, path, rename
import re
import datetime
from helpers import ensure_dirs, ensure_consistency
import pandas as pd
from collections import defaultdict


URL = 'https://raw.githubusercontent.com/mauforonda/covid19-bolivia/master/data.json'


def scrape_bolivia():
    cwd = getcwd()
    bolivia_dir = path.join(cwd, 'data', 'bolivia')
    tmp_dir = path.join(cwd, 'tmp')
    ensure_dirs(bolivia_dir, tmp_dir)

    data = requests.get(URL).json()

    for key, iso in REGION_ISO.items():
        region_data = defaultdict(dict)
        for entry in data['confirmados']:
            region_data[entry['fecha']]['cases'] = entry['dep'][key]
        for entry in data['decesos']:
            region_data[entry['fecha']]['deaths'] = entry['dep'][key]
        for entry in data['recuperados']:
            region_data[entry['fecha']]['recovered'] = entry['dep'][key]
        for date in region_data.keys():
            region_data[date]['date'] = date
            region_data[date]['region_iso'] = iso
            region_data[date]['region'] = ISO_REGION[iso]
            region_data[date]['province'] = ''
            region_data[date]['city'] = ''
            region_data[date]['place_type'] = 'departamento'
        df = pd.DataFrame(region_data.values(), columns=[
                          'date', 'region_iso', 'region', 'province', 'city', 'place_type', 'cases', 'deaths', 'recovered'])
        region_file = path.join(bolivia_dir, f'{iso.lower()}.csv')
        df.to_csv(region_file, index=False, float_format='%.f')

    with open(path.join(getcwd(), 'data', 'bolivia', 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents())


def get_readme_contents():
    toc = [f'| {name} | [`{iso.lower()}.csv`]({iso.lower()}.csv) |' for iso,
           name in ISO_REGION.items()]
    toc_contents = '\n'.join(toc)

    return f"""## Bolivia

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Region | Dataset |
| ------ | ------- |
{toc_contents}

"""


REGION_ISO = {
    "la_paz": "lp",
    "cochabamba": "cb",
    "santa_cruz": "sc",
    "oruro": "or",
    "potosí": "pt",
    "tarija": "tj",
    "chuquisaca": "ch",
    "beni": "bn",
    "pando": "pn"
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
