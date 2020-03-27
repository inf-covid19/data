import requests
from os import getcwd, path, rename

import datetime
from helpers import ensure_dirs

DATA_PER_COUNTY = 'https://services5.arcgis.com/fsYDFeRKu1hELJJs/arcgis/rest/services/FOHM_Covid_19_FME_1/FeatureServer/0/query?f=json&where=Region%20%3C%3E%20%27dummy%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Region%20asc&outSR=102100&resultOffset=0&resultRecordCount=25&cacheHint=true'

ALL_TIME_CASES_PER_COUNTY = 'https://services5.arcgis.com/fsYDFeRKu1hELJJs/arcgis/rest/services/FOHM_Covid_19_FME_1/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Statistikdatum%20desc&outSR=102100&resultOffset=0&resultRecordCount=2000&cacheHint=true'
CASES_PER_COUNTY = 'https://services5.arcgis.com/fsYDFeRKu1hELJJs/arcgis/rest/services/FOHM_Covid_19_FME_1/FeatureServer/0/query?f=json&where=Region%20%3C%3E%20%27dummy%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=Region&orderByFields=value%20desc&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Totalt_antal_fall%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true'


DEATHS_BY_AGE = 'https://services5.arcgis.com/fsYDFeRKu1hELJJs/arcgis/rest/services/FOHM_Covid_19_FME_1/FeatureServer/4/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=%C3%85ldersgrupp2&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Totalt_antal_avlidna%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&cacheHint=true'
CASES_BY_AGE = 'https://services5.arcgis.com/fsYDFeRKu1hELJJs/arcgis/rest/services/FOHM_Covid_19_FME_1/FeatureServer/4/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=%C3%85ldersgrupp2&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Totalt_antal_fall%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&cacheHint=true'

def scrape_sweden():
    cwd = getcwd()
    sweden_dir = path.join(cwd, 'data', 'sweden')
    tmp_dir = path.join(cwd, 'tmp')
    ensure_dirs(sweden_dir, tmp_dir)

    today = str(datetime.date.today())
    r = requests.get(DATA_PER_COUNTY)
    data = r.json()

    updated_county_files = []
    header = 'date,county,county_iso,city,place_type,confirmed,deaths,estimated_population_2019,area_km2,confirmed_per_100k_inhabitants,critical\n'

    for feat in data['features']:
        attributes = feat['attributes']

        county = attributes['Region']
        iso = COUNTY_ISO_MAPPED[county].lower()
        confirmed = attributes['Totalt_antal_fall']
        deaths = attributes['Totalt_antal_avlidna']
        confirmed_per_100k = attributes['Fall_per_100000_inv']
        critical = attributes['Totalt_antal_intensivvårdade']

        line = ','.join([
            today,
            county,
            iso.upper(),
            '',
            'county',
            str(confirmed),
            str(deaths),
            str(COUNTY_POPULATION_MAPPED[county]),
            str(COUNTY_AREA_MAPPED[county]),
            str(confirmed_per_100k),
            str(critical) if critical is not None else '',
        ])

        county_file = path.join(sweden_dir, f'{iso}.csv')
        is_empty = not path.exists(county_file)

        with open(county_file, 'a+') as f:
            if is_empty:
                f.write(header)
            f.write(f'{line}\n')

        if not is_empty:
            updated_county_files.append(county_file)

    for county_file in updated_county_files:
        tmp_file = path.join(tmp_dir, 'tmp-county-sweden.csv')
        rename(county_file, tmp_file)

        with open(tmp_file, 'r') as tmp_f:
            with open(county_file, 'a+') as county_f:
                header = ''
                prev_data = None
                curr_line = ''
                for line in tmp_f:
                    if header == '':
                        header = line
                        county_f.write(header)
                        continue
                    data = line.split(',')[:5]
                    if prev_data is not None and prev_data != data:
                        county_f.write(curr_line)
                    curr_line = line
                    prev_data = data
                county_f.write(curr_line)



COUNTY_ISO_MAPPED = {
    'Stockholm': 'SE-AB',
    'Västerbotten': 'SE-AC',
    'Norrbotten': 'SE-BD',
    'Uppsala': 'SE-C',
    'Sörmland': 'SE-D',
    'Östergötland': 'SE-E',
    'Jönköping': 'SE-F',
    'Kronoberg': 'SE-G',
    'Kalmar': 'SE-H',
    'Gotland': 'SE-I',
    'Blekinge': 'SE-K',
    'Skåne': 'SE-M',
    'Halland': 'SE-N',
    'Västra Götaland': 'SE-O',
    'Värmland': 'SE-S',
    'Örebro': 'SE-T',
    'Västmanland': 'SE-U',
    'Dalarna': 'SE-W',
    'Gävleborg': 'SE-X',
    'Västernorrland': 'SE-Y',
    'Jämtland Härjedalen': 'SE-Z',
}

COUNTY_AREA_MAPPED = {
    'Stockholm': 6519.3,
    'Västerbotten': 55186.2,
    'Norrbotten': 98244.8,
    'Uppsala': 8207.2,
    'Sörmland': 6102.3,
    'Östergötland': 10602.0,
    'Jönköping': 10495.1,
    'Kronoberg': 8466.0,
    'Kalmar': 11217.8,
    'Gotland': 3151.4,
    'Blekinge': 2946.4,
    'Skåne': 11034.5,
    'Halland': 5460.7,
    'Västra Götaland': 23948.8,
    'Värmland': 17591.0,
    'Örebro': 8545.6,
    'Västmanland': 5145.8,
    'Dalarna': 28188.8,
    'Gävleborg': 18198.9,
    'Västernorrland': 21683.8,
    'Jämtland Härjedalen': 49341.2
}

# http://citypopulation.de/en/sweden/cities/mun/
COUNTY_POPULATION_MAPPED = {
    'Stockholm': 2344124,
    'Västerbotten': 270154,
    'Norrbotten': 250497,
    'Uppsala': 376354,
    'Sörmland': 294695,
    'Östergötland': 461583,
    'Jönköping': 360825,
    'Kronoberg': 199886,
    'Kalmar': 244670,
    'Gotland': 59249,
    'Blekinge': 159684,
    'Skåne': 1362164,
    'Halland': 329354,
    'Västra Götaland': 1709814,
    'Värmland': 281482,
    'Örebro': 302252,
    'Västmanland': 273929,
    'Dalarna': 287191,
    'Gävleborg': 286547,
    'Västernorrland': 245453,
    'Jämtland Härjedalen': 130280,
}
