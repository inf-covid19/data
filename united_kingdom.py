import pandas as pd
import numpy as np
from os import getcwd, path
import datetime

from helpers import ensure_dirs


DEATHS_BY_AREA = 'https://cdn.jsdelivr.net/gh/emmadoughty/Daily_COVID-19/Data/deaths_by_area.csv'
CASES_BY_AREA = 'https://cdn.jsdelivr.net/gh/emmadoughty/Daily_COVID-19/Data/cases_by_area.csv'


def scrape_united_kingdom():
    cwd = getcwd()
    uk_dir = path.join(cwd, 'data', 'united_kingdom')
    ensure_dirs(uk_dir)

    headers = ['date', 'country', 'region',
               'place_type', 'geo_code', 'cases', 'deaths']

    deaths_df = pd.read_csv(DEATHS_BY_AREA, parse_dates=[0], dayfirst=True)
    deaths_df = deaths_df.set_index(['GSS_CD', 'date'])

    df = pd.read_csv(CASES_BY_AREA, parse_dates=[0], dayfirst=True)
    df = df.rename(columns={
        'GSS_CD': 'geo_code',
        'type': 'place_type',
        'confirm': 'cases',
        'area': 'region',
    })
    df['place_type'] = df.apply(lambda r: r['place_type'].lower().replace(' ', '_'), axis=1)
    df = df.sort_values(by=['country', 'region', 'date'],
                        ascending=[True, True, False])

    def fill_deaths(row):
        key = (row['geo_code'], row['date'])
        if not key in deaths_df.index:
            return np.NaN
        return deaths_df.loc[key]['deaths']

    df['deaths'] = df.apply(fill_deaths, axis=1)
    
    df = df[headers]

    countries = {}

    for country in df['country'].unique():
        is_country_data = df['region'] == country
        is_not_country_data = df['region'] != country
        is_current_country = df['country'] == country
        country_filename = country.lower().replace(' ', '_') + '.csv'
        country_file = path.join(uk_dir, country_filename)
        countries[country] = country_filename

        country_df = df[is_country_data]
        country_df.to_csv(country_file, index=False, float_format='%.f')

        regions_df = df[is_current_country & is_not_country_data]
        regions_df.to_csv(country_file, index=False,
                          header=False, float_format='%.f', mode='a')

    with open(path.join(uk_dir, 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents(countries))


def get_readme_contents(countries):
    toc = [f'| {name} | [`{csv}`]({csv}) |' for name, csv in countries.items()]
    toc_contents = '\n'.join(toc)
    return f"""## United Kingdom

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Country | Dataset |
| ------ | ------- |
{toc_contents}
"""
