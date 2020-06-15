import requests
from bs4 import BeautifulSoup
from os import getcwd, path, rename
import re
import datetime
from helpers import ensure_dirs, ensure_consistency
import pandas as pd
from collections import defaultdict


CASES_URL = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/timeseries_prov/cases_timeseries_prov.csv'
RECOVERED_URL = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/timeseries_prov/recovered_timeseries_prov.csv'
DEATHS_URL = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/timeseries_prov/mortality_timeseries_prov.csv'


def scrape_canada():
    cwd = getcwd()
    canada_dir = path.join(cwd, 'data', 'canada')
    ensure_dirs(canada_dir)

    df_cases = pd.read_csv(CASES_URL)
    df_deaths = pd.read_csv(DEATHS_URL)
    df_recovered = pd.read_csv(RECOVERED_URL)

    data = defaultdict(lambda: defaultdict(dict))

    for _, row in df_cases.iterrows():
        date = row['date_report']
        code = row['province']
        data[code][date]['cases'] = row['cumulative_cases']

    for _, row in df_deaths.iterrows():
        date = row['date_death_report']
        code = row['province']
        data[code][date]['deaths'] = row['cumulative_deaths']

    for _, row in df_recovered.iterrows():
        date = row['date_recovered']
        code = row['province']
        data[code][date]['recovered'] = row['cumulative_recovered']


    for code, region_data in data.items():
        if code not in CODE_REGION:
            continue

        region = CODE_REGION[code]
        iso = REGION_ISO[region]
        place_type = 'province'
        if iso in TERRITORIES:
            place_type = 'territory'
        for date in region_data.keys():
            region_data[date]['date'] = date
            region_data[date]['iso'] = iso
            region_data[date]['province'] = region
            region_data[date]['city'] = ''
            region_data[date]['place_type'] = place_type
        df = pd.DataFrame(region_data.values(), columns=[
                          'date', 'iso', 'province', 'city', 'place_type', 'cases', 'deaths', 'recovered'])

        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        region_file = path.join(canada_dir, f'{iso.lower()}.csv')
        df.to_csv(region_file, index=False, float_format='%.f')

    with open(path.join(canada_dir, 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents())


def get_readme_contents():
    toc = [f'| {name} | [`{iso.lower()}.csv`]({iso.lower()}.csv) |' for name,
           iso in REGION_ISO.items()]
    toc_contents = '\n'.join(toc)

    return f"""## Canada

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Region | Dataset |
| ------ | ------- |
{toc_contents}

"""


CODE_REGION = {
    'Alberta': 'Alberta',
    'BC': 'British Columbia',
    'Manitoba': 'Manitoba',
    'New Brunswick': 'New Brunswick',
    'NL': 'Newfoundland and Labrador',
    'Nova Scotia': 'Nova Scotia',
    'Nunavut': 'Nunavut',
    'NWT': 'Northwest Territories',
    'Ontario': 'Ontario',
    'PEI': 'Prince Edward Island',
    'Quebec': 'Quebec',
    # 'Repatriated': 'Repatriated',
    'Saskatchewan': 'Saskatchewan',
    'Yukon': 'Yukon',
}


REGION_ISO = {
    'Alberta': 'AB',
    'British Columbia': 'BC',
    'Manitoba': 'MB',
    'New Brunswick': 'NB',
    'Newfoundland and Labrador': 'NL',
    'Nova Scotia': 'NS',
    'Nunavut': 'NU',
    'Northwest Territories': 'NT',
    'Ontario': 'ON',
    'Prince Edward Island': 'PE',
    'Quebec': 'QC',
    # 'Repatriated': '',
    'Saskatchewan': 'SK',
    'Yukon': 'YT',
}

TERRITORIES = ['NT', 'YT', 'NU']