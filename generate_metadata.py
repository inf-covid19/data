import time
import glob
import pandas as pd
import numpy as np
import json


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
                    'place_type': row['place_type']
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
            regions[row['region']] = {
                'name': row['region'],
                'file': region_file,
                'place_type': row['place_type']
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
                    'place_type': row['place_type']
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


def get_metadata(fn, args=None):
    result = 'Done'
    print(f'[{fn.__name__}] Starting...')
    start_time = time.time()
    r = None
    try:
        r = fn(args)
    except Exception as e:
        result = f'Failed ({e.__repr__()})'
    elapsed_time = time.time() - start_time
    print(f'[{fn.__name__}] {result} in {elapsed_time:.3f}s!')
    return r


if __name__ == "__main__":
    meta_json = get_metadata(meta_countries, args={})
    meta_json = get_metadata(meta_brazil, meta_json)
    meta_json = get_metadata(meta_spain, meta_json)
    meta_json = get_metadata(meta_sweden, meta_json)
    meta_json = get_metadata(meta_united_kingdom, meta_json)
    meta_json = get_metadata(meta_united_states_of_america, meta_json)
    meta_json = get_metadata(meta_chile, meta_json)

    with open('data/metadata.json', 'w') as file:
        file.write(json.dumps(meta_json, indent=2, ensure_ascii=False))
