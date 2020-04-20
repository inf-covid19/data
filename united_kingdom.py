import pandas as pd
import numpy as np
from os import getcwd, path
import datetime
import requests

from helpers import ensure_dirs


ENGLAND_CASES_BY_AREA = 'https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv'
DEATHS_BY_AREA = 'https://coronavirus.data.gov.uk/downloads/csv/coronavirus-deaths_latest.csv'
UK_CASES_BY_AREA = 'https://cdn.jsdelivr.net/gh/emmadoughty/Daily_COVID-19/Data/cases_by_area.csv'


def scrape_united_kingdom():
    cwd = getcwd()
    tmp_dir = path.join(cwd, 'tmp', 'united_kingdom')
    uk_dir = path.join(cwd, 'data', 'united_kingdom')
    ensure_dirs(uk_dir, tmp_dir)

    england_cases_by_area_url = requests.get(ENGLAND_CASES_BY_AREA).url
    deaths_by_area_url = requests.get(DEATHS_BY_AREA).url

    headers = ['date', 'country', 'region',
               'place_type', 'geo_code', 'cases', 'deaths']

    deaths_df = pd.read_csv(deaths_by_area_url, parse_dates=[3])
    deaths_df = deaths_df.set_index(
        ['Area name', 'Area type', 'Reporting date'])

    df = pd.read_csv(UK_CASES_BY_AREA, parse_dates=[0], dayfirst=True)
    df = df.rename(columns={
        'GSS_CD': 'geo_code',
        'type': 'place_type',
        'confirm': 'cases',
        'area': 'region',
    })
    df = df.fillna(value={'place_type': 'unknown'})

    df['place_type'] = df.apply(
        lambda r: get_place_type(r['place_type']), axis=1)
    df = df.sort_values(by=['country', 'region', 'date'],
                        ascending=[True, True, False])

    def fill_deaths(row):
        area_type = row['place_type']
        if area_type == 'country':
            area_type = 'Nation'
        key = (row['region'], area_type, row['date'])
        if not key in deaths_df.index:
            return np.NaN
        return deaths_df.loc[key]['Cumulative hospital deaths']

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

    england_df = pd.read_csv(england_cases_by_area_url, parse_dates=[3])
    england_df = england_df.rename(columns={
        'Area name': 'region',
        'Area code': 'geo_code',
        'Cumulative lab-confirmed cases': 'cases',
        'Area type': 'place_type',
        'Specimen date': 'date'
    })
    england_df = england_df.fillna(value={'place_type': 'unknown'})
    england_df['country'] = 'England'
    england_df['place_type'] = england_df.apply(
        lambda r: get_place_type(r['place_type']), axis=1)
    england_df['deaths'] = england_df.apply(fill_deaths, axis=1)
    england_df = england_df.sort_values(by=['country', 'region', 'date'],
                                        ascending=[True, True, False])

    england_df = england_df[headers]
    england_filename = 'england.csv'
    england_file = path.join(uk_dir, england_filename)
    countries['England'] = england_filename

    england_df[england_df['place_type'] == 'country'].to_csv(
        england_file, index=False, float_format='%.f')
    england_df[england_df['place_type'] != 'country'].to_csv(
        england_file, index=False, float_format='%.f', header=False, mode='a')

    with open(path.join(uk_dir, 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents(countries))


def get_readme_contents(countries):
    toc = [f'| {name} | [`{csv}`]({csv}) |' for name, csv in sorted(countries.items(), key=lambda k: k[0])]
    toc_contents = '\n'.join(toc)
    return f"""## United Kingdom

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Country | Dataset |
| ------ | ------- |
{toc_contents}
"""


PLACE_TYPE_MAPPING = {
    'nation': 'country',
    'upper_tier_local_authority': 'utla'
}


def get_place_type(val):
    actual_place_type = val.lower().replace(' ', '_')
    if actual_place_type in PLACE_TYPE_MAPPING:
        return PLACE_TYPE_MAPPING[actual_place_type]
    return actual_place_type
