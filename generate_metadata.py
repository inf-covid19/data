import time
import glob
import pandas as pd
import numpy as np
import json

from helpers import executor


def meta_countries(countries={}):
    countries_file = glob.glob('data/countries/*.csv')

    for country_file in countries_file:
        country_df = pd.read_csv(country_file)

        head = country_df.iloc[0]
        head = head.fillna('')

        country_key = head.countriesAndTerritories.strip()

        countries[country_key] = {
            'name': head.countriesAndTerritories,
            'file': country_file,
            'geoId': head.geoId,
            'countryTerritoryCode': head.countryterritoryCode,
            'regions': {}
        }

    countries = dict(sorted(countries.items(), key=lambda item: item[0]))
    return countries


def meta_brazil(countries={}):
    regions_file = glob.glob('data/brazil/*.csv')
    country = 'Brazil'
    countries[country]['config'] = {
        'metrics': {
            'cases': 'confirmed'
        }
    }

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'state', 'city', 'place_type']].drop_duplicates()

        for _, row in unique_region.iterrows():
            if row['place_type'] == 'state':
                region_key = row['state']
                regions[region_key] = {
                    'name': row['state'],
                    'place_type': row['place_type'],
                    'file': region_file
                }
            elif row['place_type'] == 'city':
                region_key = '{}:{}'.format(row['state'], row['city'])
                regions[region_key] = {
                    'name': row['city'],
                    'parent': row['state'],
                    'place_type': row['place_type'],
                    'file': region_file,
                }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


def meta_spain(countries={}):
    regions_file = glob.glob('data/spain/*.csv')
    country = 'Spain'

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'region', 'city', 'place_type', 'iso']].drop_duplicates()

        for _, row in unique_region.iterrows():
            regions[row['region']] = {
                'name': row['region'],
                'iso': row['iso'],
                'place_type': row['place_type'],
                'file': region_file,
            }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


def meta_sweden(countries={}):
    regions_file = glob.glob('data/sweden/*.csv')
    country = 'Sweden'

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'county', 'county_iso', 'place_type']].drop_duplicates()

        for _, row in unique_region.iterrows():
            regions[row['county']] = {
                'name': row['county'],
                'iso': row['county_iso'],
                'file': region_file,
                'place_type': row['place_type']
            }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


def meta_united_kingdom(countries={}):
    regions_file = glob.glob('data/united_kingdom/*.csv')
    country = 'United_Kingdom'

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'country', 'region', 'place_type']].drop_duplicates()

        for _, row in unique_region.iterrows():
            if row['place_type'] == 'country':
                region_key = row['country']
                regions[region_key] = {
                    'name': region_key,
                    'file': region_file,
                    'place_type': row['place_type']
                }
            else:
                region_key = f'{row["country"]}:{row["region"]}'
                regions[region_key] = {
                    'name': row['region'],
                    'parent': row['country'],
                    'place_type': row['place_type'],
                    'file': region_file,
                }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


def meta_united_states_of_america(countries={}):
    regions_file = glob.glob('data/united_states_of_america/*.csv')
    country = 'United_States_of_America'

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'state', 'county', 'place_type']].drop_duplicates()

        for _, row in unique_region.iterrows():
            if row['place_type'] == 'state':
                region_key = row['state']
                regions[region_key] = {
                    'name': row['state'],
                    'place_type': row['place_type'],
                    'file': region_file
                }
            elif row['place_type'] == 'county':
                region_key = '{}:{}'.format(row['state'], row['county'])
                regions[region_key] = {
                    'name': row['county'],
                    'parent': row['state'],
                    'place_type': row['place_type'],
                    'file': region_file,
                }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


def meta_chile(countries={}):
    regions_file = glob.glob('data/chile/*.csv')
    country = 'Chile'

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'region', 'province', 'city', 'place_type', 'region_iso']].drop_duplicates()

        for _, row in unique_region.iterrows():
            regions[row['region']] = {
                'name': row['region'],
                'iso': row['region_iso'],
                'place_type': row['place_type'],
                'file': region_file,
            }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


def meta_bolivia(countries={}):
    regions_file = glob.glob('data/bolivia/*.csv')
    country = 'Bolivia'

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'region', 'province', 'city', 'place_type', 'region_iso']].drop_duplicates()

        for _, row in unique_region.iterrows():
            regions[row['region']] = {
                'name': row['region'],
                'iso': row['region_iso'],
                'place_type': row['place_type'],
                'file': region_file,
            }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


def meta_argentina(countries={}):
    regions_file = glob.glob('data/argentina/*.csv')
    country = 'Argentina'

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'region', 'province', 'city', 'place_type', 'region_iso']].drop_duplicates()

        for _, row in unique_region.iterrows():
            regions[row['region']] = {
                'name': row['region'],
                'iso': row['region_iso'],
                'place_type': row['place_type'],
                'file': region_file,
            }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


def meta_ecuador(countries={}):
    regions_file = glob.glob('data/ecuador/*.csv')
    country = 'Ecuador'

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'province', 'city', 'place_type', 'iso']].drop_duplicates()

        for _, row in unique_region.iterrows():
            regions[row['province']] = {
                'name': row['province'],
                'iso': row['iso'],
                'place_type': row['place_type'],
                'file': region_file,
            }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


def meta_colombia(countries={}):
    regions_file = glob.glob('data/colombia/*.csv')
    country = 'Colombia'

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'region', 'city', 'place_type', 'iso']].drop_duplicates()

        for _, row in unique_region.iterrows():
            regions[row['region']] = {
                'name': row['region'],
                'iso': row['iso'],
                'place_type': row['place_type'],
                'file': region_file,
            }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


def meta_peru(countries={}):
    regions_file = glob.glob('data/peru/*.csv')
    country = 'Peru'

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'region', 'city', 'place_type', 'iso']].drop_duplicates()

        for _, row in unique_region.iterrows():
            regions[row['region']] = {
                'name': row['region'],
                'iso': row['iso'],
                'place_type': row['place_type'],
                'file': region_file,
            }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


def meta_uruguay(countries={}):
    regions_file = glob.glob('data/uruguay/*.csv')
    country = 'Uruguay'

    regions = {}

    for region_file in regions_file:
        region_df = pd.read_csv(region_file)

        unique_region = region_df[[
            'region', 'city', 'place_type', 'iso']].drop_duplicates()

        for _, row in unique_region.iterrows():
            regions[row['region']] = {
                'name': row['region'],
                'iso': row['iso'],
                'place_type': row['place_type'],
                'file': region_file,
            }

    regions = dict(sorted(regions.items(), key=lambda item: item[0]))
    countries[country]['regions'] = regions

    return countries


if __name__ == "__main__":
    meta_json = {}
    meta_gatherer = [
        meta_countries,
        meta_brazil,
        meta_spain,
        meta_sweden,
        meta_united_kingdom,
        meta_united_states_of_america,
        meta_chile,
        meta_bolivia,
        meta_argentina,
        meta_ecuador,
        meta_colombia,
        meta_peru,
        meta_uruguay,
    ]

    for fn in meta_gatherer:
        meta_json = executor(fn, meta_json, __fallback=meta_json)

    with open('data/metadata.json', 'w') as file:
        file.write(json.dumps(meta_json, indent=2, ensure_ascii=False))
