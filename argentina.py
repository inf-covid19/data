import requests
from bs4 import BeautifulSoup
from os import getcwd, path, rename

import datetime
from helpers import ensure_dirs, ensure_consistency, get

URL = 'https://especialess3.lanacion.com.ar/coronavirus_admin/jsons/totales_provincias_full.json'


def scrape_argentina():
    cwd = getcwd()
    argentina_dir = path.join(cwd, 'data', 'argentina')
    tmp_dir = path.join(cwd, 'tmp')
    ensure_dirs(argentina_dir, tmp_dir)

    page = requests.get(URL).json()

    updated_files = []
    header = 'date,region_iso,region,province,city,place_type,cases,deaths,recovered\n'
    for dep in page:
        if dep['provincia-key'] == 'totales':
            continue
        region = CODE_REGION[dep['provincia-key']]
        day = str(datetime.datetime.strptime(
            dep['ultima-actualizacion'], '%d/%m/%Y'))[:10]
        iso = REGION_ISO[region]
        confirmed = get(dep, 'Afectados', '0')
        deaths = get(dep, 'Muertos', '0')
        recovered = get(dep, 'Recuperados', '0')
        line = ','.join([
            day,
            iso,
            region,
            '',
            '',
            'unknown' if iso == 'UNK' else 'provincia',
            str(confirmed),
            str(deaths),
            str(recovered)
        ])

        region_file = path.join(argentina_dir, f'{iso.lower()}.csv')
        is_empty = not path.exists(region_file)

        with open(region_file, 'a+') as f:
            if is_empty:
                f.write(header)
            f.write(f'{line}\n')

        if not is_empty:
            updated_files.append(region_file)

    ensure_consistency(updated_files, lambda row: row[:5])

    with open(path.join(getcwd(), 'data', 'argentina', 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents())


def get_readme_contents():
    toc = [f'| {name} | [`{iso.lower()}.csv`]({iso.lower()}.csv) |' for name,
           iso in REGION_ISO.items()]
    toc_contents = '\n'.join(toc)

    return f"""## Argentina

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Region | Dataset |
| ------ | ------- |
{toc_contents}

"""



REGION_ISO = {
    "Buenos Aires": "BA",
    "Ciudad Autónoma de Buenos Aires": "CABA",
    "Catamarca": "CA",
    "Chaco": "CH",
    "Chubut": "CT",
    "Córdoba": "CB",
    "Corrientes": "CR",
    "Entre Rios": "ER",
    "Formosa": "FO",
    "Jujuy": "JY",
    "La Pampa": "LP",
    "La Rioja": "LR",
    "Mendoza": "MZ",
    "Misiones": "MI",
    "Neuquén": "NQ",
    "Río Negro": "RN",
    "Salta": "SA",
    "San Juan": "SJ",
    "San Luis": "SL",
    "Santa Cruz": "SC",
    "Santa Fe": "SF",
    "Santiago del Estero": "SE",
    "Tierra del Fuego": "TF",
    "Tucumán": "TU",
    "Sin definir": "UNK"
}

CODE_REGION = {
    "buenos-aires": "Buenos Aires",
    "caba": "Ciudad Autónoma de Buenos Aires",
    "catamarca": "Catamarca",
    "chaco": "Chaco",
    "chubut": "Chubut",
    "cordoba": "Córdoba",
    "corrientes": "Corrientes",
    "entre-rios": "Entre Rios",
    "formosa": "Formosa",
    "jujuy": "Jujuy",
    "la-pampa": "La Pampa",
    "la-rioja": "La Rioja",
    "mendoza": "Mendoza",
    "misiones": "Misiones",
    "neuquen": "Neuquén",
    "rio-negro": "Río Negro",
    "salta": "Salta",
    "san-juan": "San Juan",
    "san-luis": "San Luis",
    "santa-cruz": "Santa Cruz",
    "santa-fe": "Santa Fe",
    "santiago-del-estero": "Santiago del Estero",
    "tierra-del-fuego": "Tierra del Fuego",
    "tucuman": "Tucumán",
    "sin-definir": "Sin definir"
}
