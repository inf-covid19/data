import requests
from bs4 import BeautifulSoup
from os import getcwd, path, rename
import re
import datetime
from helpers import ensure_dirs, ensure_consistency
import pandas as pd
from collections import defaultdict


CASES_URL = 'https://raw.githubusercontent.com/pappubahry/AU_COVID19/master/time_series_cases.csv'
RECOVERED_URL = 'https://raw.githubusercontent.com/pappubahry/AU_COVID19/master/time_series_recovered.csv'
DEATHS_URL = 'https://raw.githubusercontent.com/pappubahry/AU_COVID19/master/time_series_deaths.csv'


def scrape_australia():
    cwd = getcwd()
    australia_dir = path.join(cwd, 'data', 'australia')
    ensure_dirs(australia_dir)

    df_cases = pd.read_csv(CASES_URL)
    df_deaths = pd.read_csv(DEATHS_URL)
    df_recovered = pd.read_csv(RECOVERED_URL)

    data = defaultdict(lambda: defaultdict(dict))

    for _, row in df_cases.iterrows():
        date = row['Date']
        for iso in ISO_REGION.keys():
            data[iso][date]['cases'] = row[iso]
    
    for _, row in df_deaths.iterrows():
        date = row['Date']
        for iso in ISO_REGION.keys():
            data[iso][date]['deaths'] = row[iso]
    
    for _, row in df_recovered.iterrows():
        date = row['Date']
        for iso in ISO_REGION.keys():
            data[iso][date]['recovered'] = row[iso]
    
    for iso, region_data in data.items():
        place_type = 'state'
        if iso in ['ACT', 'NT']:
            place_type = 'territory'
        for date in region_data.keys():
            region_data[date]['date'] = date
            region_data[date]['state_iso'] = iso
            region_data[date]['state'] = ISO_REGION[iso]
            region_data[date]['city'] = ''
            region_data[date]['place_type'] = place_type
        df = pd.DataFrame(region_data.values(), columns=['date', 'state_iso', 'state', 'city', 'place_type', 'cases', 'deaths', 'recovered'])
        region_file = path.join(australia_dir, f'{iso.lower()}.csv')
        df.to_csv(region_file, index=False, float_format='%.f')

    with open(path.join(australia_dir, 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents())


def get_readme_contents():
    toc = [f'| {name} | [`{iso.lower()}.csv`]({iso.lower()}.csv) |' for iso,
           name in ISO_REGION.items()]
    toc_contents = '\n'.join(toc)

    return f"""## Australia

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Region | Dataset |
| ------ | ------- |
{toc_contents}

"""



ISO_REGION = {
    'NSW': 'New South Wales',
    'VIC': 'Victoria',
    'QLD': 'Queensland',
    'WA': 'Western Australia',
    'SA': 'South Australia',
    'TAS': 'Tasmania',
    'ACT': 'Australian Capital Territory',
    'NT': 'Northern Territory',
}
