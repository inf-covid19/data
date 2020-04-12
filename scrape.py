import time

from countries import scrape_countries
from brazil import scrape_brazil
from sweden import scrape_sweden
from united_states_of_america import scrape_united_states_of_america
from spain import scrape_spain
from united_kingdom import scrape_united_kingdom
from chile import scrape_chile
from bolivia import scrape_bolivia
from argentina import scrape_argentina

def scrape(fn):
    result = 'Done'
    print(f'[{fn.__name__}] Starting...')
    start_time = time.time()
    try:
        fn()
    except Exception as e:
        result = f'Failed ({e.__repr__()})'
    elapsed_time = time.time() - start_time
    print(f'[{fn.__name__}] {result} in {elapsed_time:.3f}s!')


if __name__ == "__main__":
    scrape(scrape_countries)
    scrape(scrape_brazil)
    scrape(scrape_sweden)
    scrape(scrape_united_states_of_america)
    scrape(scrape_spain)
    scrape(scrape_united_kingdom)
    scrape(scrape_chile)
    scrape(scrape_bolivia)
    scrape(scrape_argentina)
