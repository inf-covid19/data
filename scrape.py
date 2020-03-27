import time

from countries import scrape_countries
from brazil import scrape_brazil
from sweden import scrape_sweden


def scrape(fn):
    result = 'Done'
    print(f'[{fn.__name__}] Starting...')
    start_time = time.time()
    try:
        fn()
    except Exception as e:
        result = f'Failed ({str(e)})'
    elapsed_time = time.time() - start_time
    print(f'[{fn.__name__}] {result} in {elapsed_time:.3f}s!')


if __name__ == "__main__":
    scrape(scrape_countries)
    scrape(scrape_brazil)
    scrape(scrape_sweden)
