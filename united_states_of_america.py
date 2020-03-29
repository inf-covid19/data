from urllib import request
from os import getcwd, path

from helpers import ensure_dirs


COUNTIES_DATASET = 'https://cdn.jsdelivr.net/gh/nytimes/covid-19-data/us-counties.csv'
STATES_DATASET = 'https://cdn.jsdelivr.net/gh/nytimes/covid-19-data/us-states.csv'

def scrape_united_states_of_america():
    cwd = getcwd()
    brazil_dir = path.join(cwd, 'data', 'united_states_of_america')
    tmp_dir = path.join(cwd, 'tmp')

    ensure_dirs(brazil_dir, tmp_dir)

    states_file = path.join(tmp_dir, 'us-states.csv')
    counties_file = path.join(tmp_dir, 'us-counties.csv')
    
    request.urlretrieve(COUNTIES_DATASET, counties_file)
    request.urlretrieve(STATES_DATASET, states_file)