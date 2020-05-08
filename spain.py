import pandas as pd
import numpy as np
from os import getcwd, path
import datetime
from helpers import ensure_dirs
from urllib import request


COUNTIES_DATASET = 'https://cnecovid.isciii.es/covid19/resources/agregados.csv'


def scrape_spain():
    cwd = getcwd()
    spain_dir = path.join(cwd, 'data', 'spain')
    tmp_dir = path.join(cwd, 'tmp')
    ensure_dirs(spain_dir, tmp_dir)

    headers = ['date', 'region', 'city',
               'place_type', 'iso', 'cases', 'deaths', 'hospitalized', 'critical', 'recovered']

    df = pd.read_csv(COUNTIES_DATASET, parse_dates=[1], dayfirst=True, encoding='iso-8859-1')
    df = df.rename(columns={
        'CCAA': 'iso',
        'FECHA': 'date',
        'CASOS': 'cases',
        'Hospitalizados': 'hospitalized',
        'UCI': 'critical',
        'Fallecidos': 'deaths',
        'Recuperados': 'recovered'
    })

    df = df[df['iso'].str.len() == 2]

    def fill_cases(row):
        cases = row['cases']
        if np.isnan(cases):
            return row['PCR+'] + row['TestAc+']
        return cases

    df['cases'] = df.apply(fill_cases, axis=1)

    df = df.sort_values(by=['iso', 'date'], ascending=[True, False])
    df['region'] = df.apply(lambda r: CCAA_ISO[r['iso']], axis=1)
    df['city'] = ''
    df['place_type'] = 'autonomous_community'
    df = df[headers]

    for iso in df['iso'].unique():
        is_current_iso = df['iso'] == iso
        region_file = path.join(spain_dir, f'es-{iso.lower()}.csv')
        current_df = df[is_current_iso]
        current_df.to_csv(region_file, index=False, float_format='%.f')

    with open(path.join(spain_dir, 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents())


def get_readme_contents():
    toc = [f'| {name} | [`es-{iso.lower()}.csv`](es-{iso.lower()}.csv) |' for iso,
           name in CCAA_ISO.items()]
    toc_contents = '\n'.join(toc)

    return f"""## Spain

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Autonomous Community | Dataset |
| ------ | ------- |
{toc_contents}
"""


CCAA_ISO = {
    'AN': 'Andalucía',
    'AR': 'Aragón',
    'AS': 'Principado de Asturias',
    'CB': 'Cantabria',
    'CE': 'Ceuta',
    'CL': 'Castilla y León',
    'CM': 'Castilla La Mancha',
    'CN': 'Canarias',
    'CT': 'Cataluña',
    'EX': 'Extremadura',
    'GA': 'Galicia',
    'IB': 'Islas Baleares',
    'MC': 'Región de Murcia',
    'MD': 'Comunidad de Madrid',
    'ML': 'Melilla',
    'NC': 'Comunidad Foral de Navarra',
    'PV': 'País Vasco',
    'RI': 'La Rioja',
    'VC': 'Comunidad Valenciana',
}
