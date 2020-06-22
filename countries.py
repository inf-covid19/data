from urllib import request
from os import getcwd, path
import datetime
import pandas as pd

from helpers import ensure_dirs

COUNTRIES_DATA = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'


def scrape_countries():
    cwd = getcwd()
    countries_dir = path.join(cwd, 'data', 'countries')
    ensure_dirs(countries_dir)

    countries = {}
    df = pd.read_excel(COUNTRIES_DATA)

    for country in df['countriesAndTerritories'].unique():
        is_country = df['countriesAndTerritories'] == country
        country_filename = country.lower().replace(' ', '_') + '.csv'
        country_file = path.join(countries_dir, country_filename)
        countries[country] = country_filename

        country_df = df[is_country]
        country_df.to_csv(country_file, index=False, float_format='%.f')

    with open(path.join(countries_dir, 'README.md'), 'w') as readme_f:
        readme_f.write(get_readme_contents(countries))


def get_readme_contents(countries):
    countries_datasets = [
        (country.replace('_', ' '), filename)
        for country, filename
        in countries.items()
    ]
    toc = [
        f'| {name} | [`{dataset}`]({dataset}) |'
        for name, dataset
        in countries_datasets
    ]
    toc_contents = '\n'.join(toc)
    return f"""## Countries

> Last updated at {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S UTC')}.


| Country | Dataset |
| ------ | ------- |
{toc_contents}
"""
